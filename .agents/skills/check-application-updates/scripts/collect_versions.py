#!/usr/bin/env python3
"""Collect local application versions and config fingerprints."""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from datetime import UTC, datetime
from pathlib import Path

TIMEOUT = 20


class StateError(ValueError):
    pass


def expand(value):
    return os.path.expanduser(os.path.expandvars(value))


def path_from(value, base):
    path = Path(expand(value))
    if not path.is_absolute():
        path = base / path
    return Path(os.path.abspath(path))


def repo_root(override):
    if override:
        root = path_from(override, Path.cwd())
        if not root.is_dir():
            raise StateError(f"repository root is not a directory: {root}")
        return root
    for start in (Path.cwd(), Path(__file__).resolve().parent):
        for candidate in (start, *start.parents):
            if (candidate / ".git").exists():
                return candidate
    raise StateError("could not locate repository root (no .git found)")


def require(value, kind, where, allow_empty=False):
    valid = isinstance(value, kind) and (allow_empty or bool(value))
    if kind is list:
        valid = valid and all(isinstance(item, str) and item for item in value)
    if not valid:
        raise StateError(f"invalid {where}")
    return value


def validate(state):
    if not isinstance(state, dict) or type(state.get("schema_version")) is not int:
        raise StateError("state must be an object with schema_version 1")
    if state["schema_version"] != 1:
        raise StateError("unsupported schema_version")
    applications = require(state.get("applications"), dict, "applications", True)

    for app_id, app in applications.items():
        where = f"applications.{app_id}"
        require(app_id, str, "application id")
        app = require(app, dict, where)
        require(app.get("name"), str, f"{where}.name")
        require(app.get("config_paths"), list, f"{where}.config_paths", True)
        tracker = require(app.get("tracker"), dict, f"{where}.tracker")
        kind = require(tracker.get("type"), str, f"{where}.tracker.type")

        if kind == "pacman":
            packages = require(
                tracker.get("packages"), list, f"{where}.tracker.packages"
            )
            if any(package.startswith("-") for package in packages):
                raise StateError(f"invalid {where}.tracker.packages")
        elif kind == "command":
            require(tracker.get("argv"), list, f"{where}.tracker.argv")
            regex = tracker.get("regex")
            if regex is not None:
                require(regex, str, f"{where}.tracker.regex")
                try:
                    pattern = re.compile(regex)
                except re.error as error:
                    raise StateError(
                        f"{where}.tracker.regex is invalid: {error}"
                    ) from error
                group = tracker.get("group", 1)
                valid_group = (
                    isinstance(group, int)
                    and not isinstance(group, bool)
                    and 0 <= group <= pattern.groups
                ) or (isinstance(group, str) and group in pattern.groupindex)
                if not valid_group:
                    raise StateError(f"{where}.tracker.group does not exist in regex")
            elif "group" in tracker:
                raise StateError(f"{where}.tracker.group requires regex")
        elif kind in ("git", "toml"):
            require(tracker.get("path"), str, f"{where}.tracker.path")
            if kind == "toml":
                key = require(tracker.get("key"), str, f"{where}.tracker.key")
                if any(not part for part in key.split(".")):
                    raise StateError(f"invalid {where}.tracker.key")
        else:
            raise StateError(f"unsupported tracker type at {where}.tracker: {kind}")
    return state


def run(argv, cwd=None, env=None):
    try:
        result = subprocess.run(
            argv,
            check=False,
            cwd=cwd,
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=TIMEOUT,
        )
    except FileNotFoundError:
        return None, f"command not found: {argv[0]}"
    except subprocess.TimeoutExpired:
        return None, f"command timed out after {TIMEOUT} seconds: {argv[0]}"
    except OSError as error:
        return None, f"could not run {argv[0]}: {error}"
    return result, None


def line(text):
    return next((item.strip() for item in text.splitlines() if item.strip()), None)


def failed(label, result):
    detail = line(result.stderr) or line(result.stdout)
    message = f"{label} exited with status {result.returncode}"
    return f"{message}: {detail}" if detail else message


def pacman(tracker):
    versions = {}
    errors = []
    selected = None
    for package in tracker["packages"]:
        result, error = run(["pacman", "-Q", package])
        if error:
            errors.append(error)
            break
        if result.returncode == 0:
            fields = result.stdout.strip().split(maxsplit=1)
            if len(fields) == 2:
                versions[fields[0]] = fields[1]
                if selected is None:
                    selected = fields
    installed = {
        "source": "pacman",
        "version": selected[1] if selected else None,
        "package": selected[0] if selected else None,
    }
    if len(versions) > 1:
        installed["candidate_versions"] = dict(sorted(versions.items()))
    if not selected and not errors:
        errors.append(
            "no candidate package is installed: " + ", ".join(tracker["packages"])
        )
    return installed, errors


def command(tracker):
    argv = [expand(item) for item in tracker["argv"]]
    installed = {"source": "command", "version": None, "argv": argv}
    env = os.environ.copy()
    env["NVIM_LOG_FILE"] = os.devnull
    try:
        with tempfile.TemporaryDirectory(prefix="app-version-") as cwd:
            result, error = run(argv, cwd=cwd, env=env)
    except OSError as error:
        return installed, [f"could not create temporary command directory: {error}"]
    if error:
        return installed, [error]

    errors = []
    output = "\n".join(
        part.strip() for part in (result.stdout, result.stderr) if part.strip()
    )
    raw = line(output)
    if raw:
        installed["raw"] = raw
    if result.returncode:
        errors.append(failed(argv[0], result))
    if "regex" in tracker:
        match = re.search(tracker["regex"], output)
        version = match.group(tracker.get("group", 1)) if match else None
        if version is None:
            errors.append("version regex did not match command output")
        else:
            installed["version"] = version.strip()
    elif raw:
        installed["version"] = raw
    else:
        errors.append("command produced no version output")
    return installed, errors


def git(tracker, root):
    path = path_from(tracker["path"], root)
    installed = {"source": "git", "version": None, "path": path.as_posix()}
    if not path.is_dir():
        return installed, [f"git path not found: {path}"]
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    head, error = run(["git", "-C", str(path), "rev-parse", "HEAD"], env=env)
    if error:
        return installed, [error]
    if head.returncode or not line(head.stdout):
        return installed, [failed("git rev-parse", head)]
    installed["version"] = line(head.stdout)

    describe, error = run(
        ["git", "-C", str(path), "describe", "--always", "--tags", "--dirty"],
        env=env,
    )
    if error:
        return installed, [error]
    if describe.returncode:
        return installed, [failed("git describe", describe)]
    description = line(describe.stdout)
    if description:
        installed.update(describe=description, dirty=description.endswith("-dirty"))
    return installed, []


def toml(tracker, root):
    path = path_from(tracker["path"], root)
    key = tracker["key"]
    installed = {"source": "toml", "version": None, "path": path.as_posix(), "key": key}
    try:
        with path.open("rb") as handle:
            value = tomllib.load(handle)
    except FileNotFoundError:
        return installed, [f"TOML path not found: {path}"]
    except (OSError, tomllib.TOMLDecodeError) as error:
        return installed, [f"could not read TOML path {path}: {error}"]
    for part in key.split("."):
        if not isinstance(value, dict) or part not in value:
            return installed, [f"TOML key not found in {path}: {key}"]
        value = value[part]
    if isinstance(value, (dict, list)):
        return installed, [f"TOML key is not a scalar in {path}: {key}"]
    installed["version"] = str(value)
    return installed, []


def display(path, root):
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def fingerprint(root, configured_paths):
    entries = {}
    paths = []
    missing = []
    errors = []
    for raw in configured_paths:
        path = path_from(raw, root)
        name = display(path, root)
        paths.append(name)
        if ".git" in path.parts:
            continue
        entries[f"P:{name}"] = b""
        if not path.exists():
            missing.append(name)
            entries[f"M:{name}"] = b""
            continue
        try:
            candidates = [path] if path.is_file() else sorted(path.rglob("*"))
            for candidate in candidates:
                relative = (
                    candidate.relative_to(path).parts if candidate != path else ()
                )
                if ".git" in relative or not candidate.is_file():
                    continue
                entries[f"F:{display(candidate, root)}"] = candidate.read_bytes()
        except OSError as error:
            errors.append(f"could not read config path {name}: {error}")
            entries[f"E:{name}"] = b""

    digest = hashlib.sha256()
    for name, content in sorted(entries.items()):
        digest.update(name.encode("utf-8", "surrogateescape") + b"\0")
        digest.update(content + b"\0")
    return digest.hexdigest(), sorted(set(paths)), sorted(set(missing)), errors


def collect(app, root):
    tracker = app["tracker"]
    collectors = {"pacman": pacman, "command": command}
    if tracker["type"] in collectors:
        installed, errors = collectors[tracker["type"]](tracker)
    elif tracker["type"] == "git":
        installed, errors = git(tracker, root)
    else:
        installed, errors = toml(tracker, root)
    config_hash, paths, missing, config_errors = fingerprint(root, app["config_paths"])
    return {
        "name": app["name"],
        "installed": installed,
        "config_fingerprint": config_hash,
        "config_paths": paths,
        "missing_paths": missing,
        "errors": sorted(errors + config_errors),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", help="tracker JSON path")
    parser.add_argument("--repo-root", help="repository root override")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        root = repo_root(args.repo_root)
        state_path = (
            path_from(args.state, Path.cwd())
            if args.state
            else root / ".app-update-tracker.json"
        )
        with state_path.open(encoding="utf-8") as handle:
            state = validate(json.load(handle))
    except (OSError, json.JSONDecodeError, StateError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    output = {
        "captured_at": datetime.now(UTC)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "applications": {
            app_id: collect(state["applications"][app_id], root)
            for app_id in sorted(state["applications"])
        },
    }
    json.dump(output, sys.stdout, indent=2 if args.pretty else None, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

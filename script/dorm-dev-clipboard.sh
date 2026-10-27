#!/usr/bin/env bash
# Two-way text clipboard sync between this laptop and dorm-dev over SSH, so
# Ctrl+V works across the Moonlight stream. Moonlight's own paste types text
# as Ctrl+Shift+U Unicode sequences, which most Linux apps do not accept.
# Entries marked by password managers (x-kde-passwordManagerHint) stay local.
# Remote commands are built locally and expanded by dorm-dev's shell.
# shellcheck disable=SC2016,SC2029
set -u

if [[ -z ${WAYLAND_DISPLAY:-} ]]; then
    echo 'WAYLAND_DISPLAY is unset; waiting for the desktop session.' >&2
    exit 1
fi

host=${DORM_DEV_HOST:-dorm-dev}
state=${XDG_RUNTIME_DIR:?}/dorm-dev-clipboard
mkdir -p "$state"
ssh_opts=(-o BatchMode=yes -o ConnectTimeout=10 -o ServerAliveInterval=30
          -o ControlMaster=auto -o "ControlPath=$state/ssh" -o ControlPersist=10m)
remote_env='export XDG_RUNTIME_DIR=/run/user/$(id -u); for s in "$XDG_RUNTIME_DIR"/wayland-[0-9]; do [ -S "$s" ] && export WAYLAND_DISPLAY=${s##*/}; done'
secret_hint=x-kde-passwordManagerHint

# Hashes of the last text sent each way stop the two watchers echoing it back.
sent=$state/sent
received=$state/received

seen() {
    [[ $1 == "$(cat "$sent" 2>/dev/null)" || $1 == "$(cat "$received" 2>/dev/null)" ]]
}

# Send the laptop clipboard (stdin) to dorm-dev.
push() {
    local tmp sum
    tmp=$(mktemp "$state/push.XXXXXX")
    cat > "$tmp"
    sum=$(sha256sum < "$tmp")
    if [[ -s $tmp ]] && ! seen "$sum" && ! wl-paste --list-types 2>/dev/null | grep -qx "$secret_hint"; then
        printf '%s\n' "$sum" > "$sent"
        ssh "${ssh_opts[@]}" "$host" "$remote_env; wl-copy >/dev/null 2>&1" < "$tmp"
    fi
    rm -f "$tmp"
}

# Copy each dorm-dev clipboard change (one base64 line each) to the laptop.
pull() {
    local line tmp sum
    ssh "${ssh_opts[@]}" "$host" "$remote_env; exec wl-paste --no-newline --type text --watch sh -c 'if wl-paste --list-types | grep -qx $secret_hint; then cat >/dev/null; echo; else base64 -w0; echo; fi'" |
    while IFS= read -r line; do
        [[ -n $line ]] || continue
        tmp=$(mktemp "$state/pull.XXXXXX")
        printf '%s' "$line" | base64 -d > "$tmp"
        sum=$(sha256sum < "$tmp")
        if [[ -s $tmp ]] && ! seen "$sum"; then
            printf '%s\n' "$sum" > "$received"
            wl-copy < "$tmp"
        fi
        rm -f "$tmp"
    done
}

if [[ ${1:-} == push ]]; then
    push
    exit
fi

rm -f "$sent" "$received"
# Start from the laptop's clipboard, then follow changes on both sides.
wl-paste --no-newline --type text 2>/dev/null | push
wl-paste --no-newline --type text --watch "$0" push &
pull &
trap 'kill $(jobs -p) 2>/dev/null' EXIT
# Stop when either direction ends; the service restarts the sync.
wait -n

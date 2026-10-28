#!/usr/bin/fish --no-config
for dependency in curl jq
    if not command -q $dependency
        printf 'Network check failed: %s is required for the proxy check.\n' $dependency >&2
        exit 1
    end
end

# Prefer the service socket, then the app socket, then the legacy location.
set -l data_home $HOME/.local/share
if set -q XDG_DATA_HOME[1]; and test -n "$XDG_DATA_HOME"
    set data_home $XDG_DATA_HOME
end
set -l socket /tmp/verge/verge-mihomo.sock
for candidate in /run/clash-verge-service/users/(id -u)/verge-mihomo.sock $data_home/io.github.clash-verge-rev.clash-verge-rev/verge-mihomo.sock $socket
    if test -S "$candidate"
        set socket $candidate
        break
    end
end

# Clash Verge Rev exposes this local API without needing its API secret.
set -l api --silent --show-error --fail --noproxy '*' --max-time 3 --unix-socket $socket
set -l configs (command curl -q $api http://localhost/configs | string collect)
if test $pipestatus[1] -ne 0
    printf 'Network check failed: cannot read the running Clash configuration.\n' >&2
    exit 1
end
if not printf '%s' "$configs" | command jq -e '.mode == "global" and .tun.enable == true' >/dev/null
    printf 'Network check failed: enable Clash TUN and switch to Global mode.\n' >&2
    exit 1
end

set -l proxies (command curl -q $api http://localhost/proxies | string collect)
if test $pipestatus[1] -ne 0
    printf 'Network check failed: cannot read the selected Clash route.\n' >&2
    exit 1
end
set -l route_filter '
    .proxies as $proxies |
    def selected($name; $seen):
        if ($seen | index($name)) != null then error("proxy selection cycle")
        else $proxies[$name] as $node |
            if ($node | type) != "object" then error("missing selected proxy")
            elif $node.type == "Selector" then
                selected($node.now; $seen + [$name])
            elif ($node | has("all") or has("now")) then
                error("select a fixed Taiwan node instead of an automatic group")
            elif (["Direct", "Reject", "RejectDrop", "Compatible", "Pass"] | index($node.type)) != null
                or ($node.type | type) != "string" then error("selected route is not a proxy")
            elif ($name | test("台湾|台灣|taiwan|(^|[^a-z])tw([^a-z]|$)|🇹🇼"; "i") | not) then
                error("select a Taiwan node in GLOBAL")
            else {name: $name, type: $node.type} end
        end;
    selected("GLOBAL"; [])'
set -l route (printf '%s' "$proxies" | command jq -cer "$route_filter")
or exit 1

printf 'Clash check passed: TUN enabled; Global → %s\n' (printf '%s' "$route" | command jq -r .name) >&2

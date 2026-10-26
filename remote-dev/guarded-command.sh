#!/usr/bin/bash
# Start an agent CLI only while Mihomo routes through the fixed Taiwan node.
# Linked as ~/.local/guarded-bin/{claude,codex,t3}; runs ~/.local/bin/<name>.
set -e
name=$(basename "$0")
if [[ ! -x /usr/local/libexec/mihomo-route.py ]]; then
    echo 'Agent startup blocked: finish the Mihomo system setup first.' >&2
    exit 1
fi
/usr/bin/python /usr/local/libexec/mihomo-route.py check
if [[ ${1:-} == --proxy-check ]]; then
    exit 0
fi
exec "$HOME/.local/bin/$name" "$@"

#!/bin/sh

# Keep the existing lid-toggle entry point.
exec "$(dirname "$0")/toggle-inhibit.sh" lid

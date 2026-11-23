#!/usr/bin/env bash
# Open the talk in marimo with no login token (localhost only).
cd "$(dirname "$0")"
exec .venv/bin/marimo edit talk.py --no-token "$@"

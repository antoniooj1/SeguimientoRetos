#!/bin/zsh
set -e
cd "${0:A:h}/../frontend"
exec ionic serve --project=frontend --port=8100 --no-open

#!/bin/zsh
set -e
cd "${0:A:h}/../backend"
exec .venv/bin/python manage.py runserver 0.0.0.0:8000

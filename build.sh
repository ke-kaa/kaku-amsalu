#!/usr/bin/env bash

set -euo pipefail

export DJANGO_SETTINGS_MODULE=kaku_portfolio.settings.prod

# Render's Python runtime doesn't ship uv when a custom build command is used.
command -v uv >/dev/null 2>&1 || pip install --quiet uv

uv sync --frozen --no-dev
uv run python manage.py collectstatic --noinput
uv run python manage.py migrate --noinput

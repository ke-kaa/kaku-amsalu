#!/usr/bin/env bash

set -o exiterror

uv sync --clean --verbose --no-optional --no-dev --no-bin-links --no-lockfile --no-save && \
uv run python manage.py collectstatic --noinput --settings=kaku_portfolio.settings.prod  && \
uv run python manage.py migrate --noinput --settings=kaku_portfolio.settings.prod


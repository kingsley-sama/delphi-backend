#!/usr/bin/env zsh
source .venv/bin/activate
docker start postgres-dev
code .
uv run app/main.py
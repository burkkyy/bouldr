#!/bin/sh

set -e

uv sync --frozen

# Run initializers in environment then start the application
if [ "$NODE_ENV" != "production" ]; then
    uv run python ./src/initializers/main.py
    uv run flask --app ./src/server.py run --host=0.0.0.0 --port=5000
else
    echo "Running in production mode is NOT IMPLEMENTED"
    exit 1
fi
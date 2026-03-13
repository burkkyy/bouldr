#!/bin/sh

set -e

uv sync --frozen

# Run initializers in environment then start the application
if [ "$NODE_ENV" != "production" ]; then
    # If you can find a better way to do this, please let me know
    PYTHONPATH=. uv run flask --app ./src/app.py run --host=0.0.0.0 --port=5001
else
    echo "Running in production mode is NOT IMPLEMENTED"
    exit 1
fi
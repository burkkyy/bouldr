#!/bin/sh

# Run initializers in environment then start the application
if [ "$NODE_ENV" != "production" ]; then
    # If you can find a better way to do this, please let me know
    cd dist/
    PYTHONPATH=. uv run python src/app.py
else
    # For the csci lab machines
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        .venv/bin/pip install .
    fi

    PYTHONPATH=. .venv/bin/python src/app.py
fi
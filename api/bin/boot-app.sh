#!/bin/sh

# Run initializers in environment then start the application
if [ "$NODE_ENV" != "production" ]; then
    # If you can find a better way to do this, please let me know
    PYTHONPATH=. uv run python src/app.py
else
    cd dist/
    PYTHONPATH=. uv run python src/app.py
fi
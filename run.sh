#!/usr/bin/env bash
set -e

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
    echo "No .env found — copy .env.example to .env and add your API key first."
    exit 1
fi

python -m app.main "$@"
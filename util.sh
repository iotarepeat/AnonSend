#!/usr/bin/env bash
if [[ $1 == "clean" ]]
then
    find . -name '*.pkl' -type f -exec rm -rf {} +
    rm -rf 'db.sqlite3'
    find . -name '__pycache__' -type d -exec rm -rf {} +
    find ./main/migrations/ ! -name '__init__.py' -delete 2>/dev/null
fi
if [[ $1 == "build" ]]; then
    python3 manage.py makemigrations && python3 manage.py migrate
fi

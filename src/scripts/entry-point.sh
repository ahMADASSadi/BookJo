#!/bin/bash

source env.sh

WORKERS=$(python -c "import os; print(os.cpu_count())")
PORT=$(python -c "import os; print(os.getenv('PORT', '8000'))")
python manage.py migrate

python manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:"$PORT" --workers "$WORKERS" config.wsgi:application
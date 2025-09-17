#!/bin/sh

set -e

# WORKERS=$(python -c "import os; print(os.cpu_count())")
# PORT=$(python -c "import os; print(os.getenv('PORT', '8000'))")
echo "Applying database migrations..."
python manage.py migrate --noinput

python manage.py collectstatic --noinput

# gunicorn --bind 0.0.0.0:"$PORT" --workers "$WORKERS" config.wsgi:application

exec "$@"

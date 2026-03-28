#!/bin/sh
# Entrypoint script: waits for MySQL, initializes DB, then starts uvicorn

set -e

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-3306}"
DB_USER="${DB_USER:-trader}"
DB_PASSWORD="${DB_PASSWORD:-traderpass}"

echo "Waiting for MySQL at $DB_HOST:$DB_PORT..."
until mysqladmin ping -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" --ssl=0 --silent 2>/dev/null; do
  echo "MySQL not ready - retrying..."
  sleep 2
done

echo "MySQL is ready!"

echo "Running database migrations..."
# ensure application package is importable by Alembic
cd /app || exit 1
export PYTHONPATH=/app
/usr/local/bin/alembic upgrade head || {
  echo "Failed to run migrations, but continuing...";
}

echo "Starting gunicorn with uvicorn workers..."
if [ "$#" -gt 0 ]; then
  echo "Received command: $@ — running it"
  exec "$@"
else
  exec /usr/local/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --access-logfile - --error-logfile - app.main:app
fi

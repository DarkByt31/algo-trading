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

echo "Initializing database tables..."
python -c "from app.db.base import Base; from app.db.session import engine; Base.metadata.create_all(bind=engine)" || {
  echo "Failed to initialize DB, but continuing...";
}

echo "Starting uvicorn..."
if [ "$#" -gt 0 ]; then
  echo "Received command: $@ — running it"
  exec "$@"
else
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi

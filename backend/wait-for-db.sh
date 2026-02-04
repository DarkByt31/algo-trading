#!/bin/sh
# Wait for MySQL to be ready before starting the application
# Usage: ./wait-for-db.sh <host> <port> <command>

set -e

HOST=${1:-db}
PORT=${2:-3306}
USER=${3:-trader}
PASSWORD=${4:-traderpass}

shift 4
CMD="$@"

echo "Waiting for MySQL at $HOST:$PORT..."

until mysqladmin ping -h "$HOST" -P "$PORT" -u "$USER" -p"$PASSWORD" --silent; do
  echo "MySQL is unavailable - sleeping..."
  sleep 2
done

echo "MySQL is up - executing command..."
exec $CMD

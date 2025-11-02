#!/bin/sh
set -e

# Fix permissions on data directory (for Docker volume mounted at /app/data)
# This needs to run as root before switching to appuser
if [ -d /app/data ]; then
    echo "Fixing permissions on /app/data..."
    chown -R appuser:appuser /app/data
    chmod -R 755 /app/data
fi

# Switch to appuser and execute the command passed to docker run
echo "Starting application as appuser..."
exec gosu appuser "$@"

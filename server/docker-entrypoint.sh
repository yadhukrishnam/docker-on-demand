#!/bin/bash
set -euo pipefail

WORKERS=${WORKERS:-1}
ACCESS_LOG=${ACCESS_LOG:--}
ERROR_LOG=${ERROR_LOG:--}
WORKER_TEMP_DIR=${WORKER_TEMP_DIR:-/dev/shm}
SECRET_KEY=${SECRET_KEY:-}

# Check that a .secret_key file or SECRET_KEY envvar is set
if [ ! -f .secret_key ] && [ -z "$SECRET_KEY" ]; then
    if [ $WORKERS -gt 1 ]; then
        echo "[ ERROR ] You are configured to use more than 1 worker."
        echo "[ ERROR ] To do this, you must define the SECRET_KEY environment variable or create a .secret_key file."
        echo "[ ERROR ] Exiting..."
        exit 1
    fi
fi

# Start
echo "Starting Docker-on-Demand"
exec gunicorn 'app:app' \
    --bind '0.0.0.0:1337' \
    --workers $WORKERS \
    --worker-tmp-dir "$WORKER_TEMP_DIR" \
    --access-logfile "$ACCESS_LOG" \
    --error-logfile "$ERROR_LOG"

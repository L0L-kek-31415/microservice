#!/bin/sh

echo "Waiting for rabbitmq..."

while ! nc -z "rabbitmq" "5672"; do
  sleep 0.1
done

echo "rabbitmq started"

uvicorn main:app --host 0.0.0.0 --port 8002

exec "$@"
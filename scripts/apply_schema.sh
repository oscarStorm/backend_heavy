#!/usr/bin/env bash

until docker exec backend-heavy-mysql \
  mysqladmin ping -h 127.0.0.1 -u admin -pfrigus7913 --silent; do
  echo "Waiting for MySQL..."
  sleep 1
done

docker exec -i backend-heavy-mysql \
  mysql -h 127.0.0.1 -u admin -pfrigus7913 backend_heavy <sql/schema.sql

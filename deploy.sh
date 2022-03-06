#!/bin/bash
docker rm server_manager --force
set -e
docker build . -t server_manager
docker-compose down
docker-compose up -d
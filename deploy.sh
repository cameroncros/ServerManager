#!/bin/bash
docker rm server_manager --force
set -e
docker build . -t server_manager
docker run -d --restart always --net=host --mount type=bind,source="$(pwd)"/id_rsa,target=/app/id_rsa --name server_manager server_manager

#!/bin/bash

echo "Changing the scale for the container apps to 5"

docker-compose up -d --scale app_1=5
#!/bin/bash

echo "give a number of scale:"
read scale_number

docker-compose up -d --scale app_1=$scale_number
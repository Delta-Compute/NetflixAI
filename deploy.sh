#!/bin/bash
# Simple deployment script

docker-compose build && docker-compose up -d

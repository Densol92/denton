#!/usr/bin/env bash
docker  build -t denton:latest .
docker run --rm -t denton --daily
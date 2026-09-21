#!/usr/bin/env bash
set -euo pipefail
docker build -t observability-demo:local ./app
kind load docker-image observability-demo:local --name observability

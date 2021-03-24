#!/usr/bin/env bash

# Print commands and their arguments as they are executed.
set -x

# mypy thingooConnector
black thingooConnector --check
isort --check-only thingooConnector
flake8 thingooConnector
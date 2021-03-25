#!/usr/bin/env bash

# Exit immediately if command exits with a non-zero status.
set -e

# Print commands and their arguments as they are executed.
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place thingooConnector --exclude=__init__.py
black thingooConnector
isort thingooConnector
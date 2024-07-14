#!/bin/bash

# immediately exit if any command has a non-zero exit status
set -e

python /app/source/knowledge_base_init.py
python /app/source/app.py
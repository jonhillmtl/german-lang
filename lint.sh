#!/usr/bin/env bash

set -e
set -v

python3 -m pyflakes pipe_to main.py setup.py tests.py

# typechecks
python3 -m mypy \
  --disallow-untyped-defs \
  --warn-unused-ignores \
  --ignore-missing-imports \
  --strict-optional \
  .

pycodestyle --max-line-length=110 pipe_to main.py setup.py tests.py
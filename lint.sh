#!/usr/bin/env bash

set -e
set -v

# lint it using pyflakes
# python3 -m pyflakes `find . -name "*.py"`

pycodestyle --max-line-length=140 .

# enforce docstrings
pep257 --add-ignore=D202,D210,D200

# typechecks
python3 -m mypy \
    --warn-unused-ignores \
    --ignore-missing-imports \
    --strict-optional \
    --disallow-untyped-defs `find . -name "*.py"`

# and now just to be really hard on yourself
pylint `find . -name "*.py"` \
    --max-line-length=140 \
    -d C0111 -d W0511 -d R0904 -d R0912 -d C0411 \
    -d R0914 -d R0913 -d C0330 -d R0801 -d R0915

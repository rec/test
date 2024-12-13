#!/bin/bash

# Upgrades a project using lintrunner to use Python 3.9 style annotations
# Uses this Python script:
# https://github.com/rec/test/blob/master/python/add_annotations.py

python ~/code/test/python/add_annotations.py $@
pyupgrade --py39-plus $@
ruff check --select TCH --unsafe-fixes --fix $@
lintrunner -a --take=RUFF
lintrunner -a --take=RUFF

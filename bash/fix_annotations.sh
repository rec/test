#!/bin/bash

# Upgrades a project using lintrunner to use Python 3.9 style annotations

python ~/code/test/python/add_annotations.py $@
pyupgrade --py39-plus $@
ruff check --select TCH --unsafe-fixes --fix $@
lintrunner -a --take=RUFF
lintrunner -a --take=RUFF

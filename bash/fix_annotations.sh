#!/bin/bash

python ~/code/test/python/add_annotations.py $@
pyupgrade --py39-plus $@
ruff check --select TCH --unsafe-fixes --fix $@

#!/bin/bash

set -ex

root=/Users/tom/synthetic/code/test/python/.direnv/python-3.12/bin/

$root/mypy *.py setlint/
$root/ruff check --fix
$root/ruff format
$root/pytest -vvvv
$root/python -m setlint /code/pytorch/torch/_inductor --fix

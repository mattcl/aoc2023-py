#!/bin/sh
set -e

poetry build

pipx install -f dist/mattcl_aoc2023_py*.tar.gz

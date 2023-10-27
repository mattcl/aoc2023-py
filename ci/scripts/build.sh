#!/bin/sh
set -e

# This script can pretty much do whatever, but the most basic thing would be
# ensuring the project's dependencies are installable and that the tests and
# benchmarks run

poetry install

# Without filtering any of the marks, this should run the example and real input
# tests as well as running the benchmarks.
poetry run pytest

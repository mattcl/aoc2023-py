#!/bin/bash
set -e

# this is expected to be run from the root of the project, as it makes
# assumptions about the paths


if [ -z ${1+x} ]; then
    echo "script must be provided an integer day as an argument"
    exit 1
fi

# make a padded day
printf -v PADDED_DAY "%02d" "$1"

echo "> creating files for ${PADDED_DAY}"
MOD_NAME="aoc/day${PADDED_DAY}.py"
TEST_NAME="tests/test_day${PADDED_DAY}.py"
INPUT_NAME="inputs/day${PADDED_DAY}.txt"
EXAMPLE_NAME="inputs/day${PADDED_DAY}_example.txt"

# copy the module template for the given day to a new module
cp aoc/template.py "$MOD_NAME"

# copy the test template for the given day to a new test file
cp tests/template.py "$TEST_NAME"

# make empty input files
touch "$INPUT_NAME"
touch "$EXAMPLE_NAME"

echo "> replacing markers"
# replace the DAY makers with the current day
sed -i "s/DAY/$PADDED_DAY/g" "$MOD_NAME"
sed -i "s/DAY/$PADDED_DAY/g" "$TEST_NAME"

echo "> done"

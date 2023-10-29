# make the modules/files/tests for a new day's problem
new DAY:
    scripts/new.sh {{DAY}}

# run the unit tests (against example inputs)
unit:
    poetry run pytest tests -m "not bench and not real"

# run all tests except benchmarks
test:
    poetry run pytest tests -m "not bench"

# run all benchmarks
bench:
    poetry run pytest tests -m "bench"

# run all tests and benchmarks
all:
    poetry run pytest tests

# run all tests and benchmarks
watch:
    poetry run ptw . -m "not bench and not real"

# run the solver for the given DAY and INPUT
run DAY INPUT:
    poetry run mattcl-aoc-py {{DAY}} {{INPUT}}

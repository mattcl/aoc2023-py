# 2023 Advent of Code Solutions

This package distributes a library named
`mattcl-aoc2023-py` that
exposes a module named `aoc` and an executable named
`mattcl-aoc` that, given a day and input, will
provide the solution.

```
mattcl-aoc 3 my_input.txt
```


This project is designed to be compatible with a [comparative benchmarking
pipeline](https://github.com/mattcl/aoc-ci-bencher/blob/master/SPECIFICATION.md),
which explains some of the layout and design decisions.


## Developing

### Prerequisites

1. python >=3.10, <3.13 (3.12 preferred) (recommended install via
   [pyenv](https://github.com/pyenv/pyenv) or equivalent)
2. [poetry](https://python-poetry.org/docs/#installing-with-pipx) 1.6.1 or
   compatible (recommended install via [pipx](https://pypa.github.io/pipx/))
3. _Optionally_ [just](https://github.com/casey/just#packages) for convenience commands
4. _Optionally_ docker


This project is managed by `poetry`, so the environment is set up by running
`poetry install`, and packages are managed via `poetry update` and `poetry
lock`. The `poetry.lock` _should_ be checked in, as this repo distributes an
executable.

You can switch into the context of the created virtualenv by running `poetry
shell`.


### Naming conventions

Solutions for a given day should be exposed by a module with name `day<formatted
number>`, where `<formatted number>` is a zero-padded (width 2) integer
corresponding to the day (e.g. `day05` or `day15`). The zero-padding is mainly
to maintain a sorted ordering visually. These modules should exist directly
under the top-level `aoc` directory (the project module).

Inputs should follow the same naming convention, with inputs located
under the top-level `inputs` directory with the names `day01.txt`,
`day01_example.txt`, `day02.txt`, etc.

Tests have no naming restrictions, and are located under the top-level `tests`
directory.


### Running a solution for a given day


```
# with plain poetry
poetry run mattcl-aoc DAY PATH_TO_INPUT

# with poetry shell activated (or if you just installed the distribution)
mattcl-aoc DAY PATH_TO_INPUT

# example
mattcl-aoc 2 inputs/day02.txt
```

For information on how the CLI works see [aoc/cli.py](aoc/cli.py).


### Running tests

Test cases are marked with `@pytest.mark.example`, `@pytest.mark.real`, and
`@pytest.mark.bench` to indicate if they are tests against example input, real
inputs, or benchmarks, respectively. Tests can be selected or filtered using the
normal `pytest`
[arguments](https://docs.pytest.org/en/latest/example/markers.html#mark-run).

The reason tests are marked differently is to allow for faster test runs while
developing by excluding known-slow tests like tests against real inputs and
benchmarks.

Filesystem watching support is provided with
[`pytest-watcher`](https://github.com/olzhasar/pytest-watcher).

Benchmark support is provided with
[`pytest-benchmark`](https://pypi.org/project/pytest-benchmark/).


### Running all tests and benchmarks

```
# with plain poetry
poetry run pytest tests

# with poetry shell activated
pytest tests

# with just
just all
```


### Running just unit tests and tests against examples

```
# with plain poetry
poetry run pytest tests -m "not bench and not real"

# with poetry shell activated
pytest tests -m "not bench and not real"

# with just
just unit
```


### Running all tests except benchmarks

```
# with plain poetry
poetry run pytest tests -m "not bench"

# with poetry shell activated
pytest tests -m "not bench"

# with just
just test
```


### Running benchmarks

```
# with plain poetry
poetry run pytest tests -m "bench"

# with poetry shell activated
pytest tests -m "bench"

# with just
just bench
```


### Running tests in response to code changes

It's recommended not to run the testing loop with benchmarks and real-input
tests because of the potential slowness, but you do you.

```
# with plain poetry
poetry run ptw . -m "not bench and not real"

# with poetry shell activated
ptw . -m "not bench and not real"

# with just
just watch

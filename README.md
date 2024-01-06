# 2023 Advent of Code Solutions

This package distributes a library named
`mattcl-aoc2023-py` that
exposes a module named `aoc` and an executable named
`mattcl-aoc-py` that, given a day and input, will
provide the solution.

```
mattcl-aoc-py 3 my_input.txt
```

This is mostly ported from my rust solutions with a similar performance goal.


## Current runtime ~1.7s

The cold-start time one a 7735HS is roughly 2.2s

With the exception of day 24 and 25, which import numpy and networkx
respectively, there are no external dependencies.

```
------ benchmark: 25 tests -------
Name (time in ms)    Mean   StdDev
----------------------------------
test_day01         1.7859   0.0349
test_day02         0.6200   0.0293
test_day03         2.7599   0.0839
test_day04         0.6197   0.0262
test_day05         1.0391   0.0323
test_day06         0.0051   0.0003
test_day07         2.5412   0.4279
test_day08         6.7066   0.6922
test_day09         1.3349   0.0495
test_day10        11.6985   0.3411
test_day11         0.5428   0.0188
test_day12        78.0007  10.9906
test_day13         1.8996   0.0626
test_day14       157.3659   2.7023
test_day15         6.6442   0.1941
test_day16       347.0442  34.7542
test_day17       286.8772   2.0432
test_day18         0.6517   0.0205
test_day19         2.3693   1.0639
test_day20       112.3589   2.0881
test_day21       173.5629   8.6991
test_day22        71.1298   8.4224
test_day23       330.0346   9.6357
test_day24        31.0174   0.6720
test_day25        54.0391  20.6532
----------------------------------

# combined
---------- benchmark: 1 tests ----------
Name (time in s)            Mean  StdDev
----------------------------------------
test_combined_runtime     1.6918  0.0361
----------------------------------------
```


This project is designed to be compatible with a [comparative benchmarking
pipeline](https://github.com/mattcl/aoc-benchmarks/blob/master/SPECIFICATION.md),
which explains some of the layout and design decisions.

Original rust solutions [here](https://github.com/mattcl/aoc2023)


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


### Starting work on a new day's problem

You can either copy the templates and create the input placeholders by yourself,
or you can run one of the following. By default, the template that generated
this project also generated the day 1 placeholder module/tests/inputs.

```
# without just
./scripts/new.sh DAY  # where DAY is 1-25

# with just
just new DAY
```


### Running a solution for a given day

```
# with plain poetry
poetry run mattcl-aoc-py DAY PATH_TO_INPUT

# with poetry shell activated (or if you just installed the distribution)
mattcl-aoc-py DAY PATH_TO_INPUT

# example
mattcl-aoc-py 2 inputs/day02.txt
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

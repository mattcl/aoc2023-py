import pytest

from aoc.day01 import Solver
from aoc.util import Solution


#############################
# ========= setup ==========#
#############################
@pytest.fixture
def example_input() -> str:
    with open("inputs/day01_example.txt", "r") as f:
        return f.read()


@pytest.fixture
def real_input() -> str:
    with open("inputs/day01.txt", "r") as f:
        return f.read()


@pytest.fixture
def example_solver(example_input: str) -> Solver:
    return Solver(example_input)


@pytest.fixture
def real_solver(real_input: str) -> Solver:
    return Solver(real_input)


#############################
# === tests for part one ===#
#############################
@pytest.mark.example
def test_example_part_one(example_solver: Solver):
    assert example_solver.part_one() == 0


@pytest.mark.real
def test_real_part_one(real_solver: Solver):
    assert real_solver.part_one() == 0


#
#############################
# === tests for part two ===#
#############################
@pytest.mark.example
def test_example_part_two(example_solver: Solver):
    assert example_solver.part_two() == 0


@pytest.mark.real
def test_real_part_two(real_solver: Solver):
    assert real_solver.part_two() == 0


#############################
# ======= benchmarks =======#
#############################
@pytest.mark.bench
def test_day01(benchmark, real_input: str):
    expected = Solution(part_one=0, part_two=0)
    result = benchmark(Solver.solve, real_input)

    # let's just leverage the diffs pytest will provide for better output
    assert result.__dict__ == expected.__dict__

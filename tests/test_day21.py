import pytest

from aoc.day21 import Solver
from aoc.util import Solution


#############################
# ======= solutons =========#
#############################
PART_ONE = 3776
PART_TWO = 625587097150084


#############################
# ========= setup ==========#
#############################
@pytest.fixture
def real_input() -> str:
    with open("inputs/day21.txt", "r") as f:
        return f.read()


@pytest.fixture
def real_solver(real_input: str) -> Solver:
    return Solver(real_input)


#############################
# === tests for part one ===#
#############################
@pytest.mark.real
def test_real_part_one(real_solver: Solver):
    assert real_solver.part_one() == PART_ONE


#############################
# === tests for part two ===#
#############################
@pytest.mark.real
def test_real_part_two(real_solver: Solver):
    assert real_solver.part_two() == PART_TWO


#############################
# ======= benchmarks =======#
#############################
@pytest.mark.bench
def test_day21(benchmark, real_input: str):
    expected = Solution(part_one=PART_ONE, part_two=PART_TWO)
    result = benchmark(Solver.solve, real_input)

    # let's just leverage the diffs pytest will provide for better output
    assert result.__dict__ == expected.__dict__

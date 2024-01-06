import pytest

from aoc.day01 import Solver as Day01
from aoc.day02 import Solver as Day02
from aoc.day03 import Solver as Day03
from aoc.day04 import Solver as Day04
from aoc.day05 import Solver as Day05
from aoc.day06 import Solver as Day06
from aoc.day07 import Solver as Day07
from aoc.day08 import Solver as Day08
from aoc.day09 import Solver as Day09
from aoc.day10 import Solver as Day10
from aoc.day11 import Solver as Day11
from aoc.day12 import Solver as Day12
from aoc.day13 import Solver as Day13
from aoc.day14 import Solver as Day14
from aoc.day15 import Solver as Day15
from aoc.day16 import Solver as Day16
from aoc.day17 import Solver as Day17
from aoc.day18 import Solver as Day18
from aoc.day19 import Solver as Day19
from aoc.day20 import Solver as Day20
from aoc.day21 import Solver as Day21
from aoc.day22 import Solver as Day22
from aoc.day23 import Solver as Day23
from aoc.day24 import Solver as Day24
from aoc.day25 import Solver as Day25
from aoc.util import Solution


def all_days(inputs):
    Day01.solve(inputs[0])
    Day02.solve(inputs[1])
    Day03.solve(inputs[2])
    Day04.solve(inputs[3])
    Day05.solve(inputs[4])
    Day06.solve(inputs[5])
    Day07.solve(inputs[6])
    Day08.solve(inputs[7])
    Day09.solve(inputs[8])
    Day10.solve(inputs[9])
    Day11.solve(inputs[10])
    Day12.solve(inputs[11])
    Day13.solve(inputs[12])
    Day14.solve(inputs[13])
    Day15.solve(inputs[14])
    Day16.solve(inputs[15])
    Day17.solve(inputs[16])
    Day18.solve(inputs[17])
    Day19.solve(inputs[18])
    Day20.solve(inputs[19])
    Day21.solve(inputs[20])
    Day22.solve(inputs[21])
    Day23.solve(inputs[22])
    Day24.solve(inputs[23])
    Day25.solve(inputs[24])


@pytest.fixture
def inputs():
    out = []
    for day in range(1, 26):
        input_file = "inputs/day{:02d}.txt".format(day)
        with open(input_file, "r") as f:
            out.append(f.read())

    return out


@pytest.mark.combined
@pytest.mark.bench
def test_combined_runtime(benchmark, inputs):
    benchmark(all_days, inputs)

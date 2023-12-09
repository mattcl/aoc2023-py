"""09: PROBLEM NAME"""
from functools import reduce
from itertools import pairwise
import aoc.util


def process(sequence):
    return list(map(lambda x: x[1] - x[0], pairwise(sequence)))


def extrapolate(sequence, diffs):
    return [sequence[0] - diffs[0], sequence[len(sequence) - 1] + diffs[1]]


def extrapolate_sequence(sequence):
    new_seq = process(sequence)

    if any(new_seq):
        diffs = extrapolate_sequence(new_seq)
        return extrapolate(sequence, diffs)
    else:
        return extrapolate(sequence, [0, 0])


def sum_diff(a, b):
    a[0] += b[0]
    a[1] += b[1]
    return a


def extrapolate_all(sequences):
    return reduce(sum_diff, map(extrapolate_sequence, sequences), [0, 0])


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        sequences = (list(map(int, line.split())) for line in input.splitlines())
        ans = extrapolate_all(sequences)
        self.left = ans[0]
        self.right = ans[1]

    def part_one(self) -> int:
        return self.right

    def part_two(self) -> int:
        return self.left

"""11: cosmic expansion"""
from copy import copy
from itertools import combinations, pairwise
import aoc.util


def axis_sum(pos_counts, expansion):
    total = 0
    distance = 0
    offset = 0
    global_idx = 0
    for idx, count in enumerate(pos_counts):
        if count == 0:
            offset += expansion
        else:
            expansion_offset = idx + offset
            for _ in range(0, count):
                distance += global_idx * expansion_offset - total
                total += expansion_offset
                global_idx += 1

    return distance


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        lines = input.splitlines()
        width = len(lines[0])
        row_counts = []
        col_counts = [0] * width

        for line in lines:
            row_count = 0
            for col, ch in enumerate(line):
                if ch == '#':
                    col_counts[col] += 1
                    row_count += 1

            row_counts.append(row_count)

        self.p1 = axis_sum(row_counts, 1) + axis_sum(col_counts, 1)
        self.p2 = axis_sum(row_counts, 999999) + axis_sum(col_counts, 999999)

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2

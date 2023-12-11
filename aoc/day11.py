"""11: cosmic expansion"""
from copy import copy
from itertools import combinations, pairwise
import aoc.util


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class Galaxy:
    def __init__(self, location):
        self.original = location
        self.one = copy(location)
        self.one_million = copy(location)


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        lines = input.splitlines()
        width = len(lines[0])
        galaxies = []
        num_empty_rows = 0
        empty_cols_raw = set(range(0, width))

        for row, line in enumerate(input.splitlines()):
            seen_row = False
            for col, ch in enumerate(line):
                if ch == '#':
                    seen_row = True
                    galaxy = Galaxy(Location(col, row))
                    galaxy.one.y += num_empty_rows
                    galaxy.one_million.y += num_empty_rows * 999999
                    galaxies.append(galaxy)
                    if col in empty_cols_raw:
                        empty_cols_raw.remove(col)

            if not seen_row:
                num_empty_rows += 1

        empty_cols = list(sorted(empty_cols_raw))
        empty_cols.append(width)

        cols_iter = list(reversed(list(enumerate(empty_cols))))

        counts = [0] * width

        for (idx1, col1), (idx2, col2) in pairwise(enumerate(empty_cols)):
            for j in range(col1, col2):
                counts[j] = idx1 + 1

        for g in galaxies:
            multiple = counts[g.original.x]
            g.one.x += multiple
            g.one_million.x += 999999 * multiple

        self.p1 = 0
        self.p2 = 0

        for a, b in combinations(galaxies, 2):
            self.p1 += a.one.manhattan_distance(b.one)
            self.p2 += a.one_million.manhattan_distance(b.one_million)

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2

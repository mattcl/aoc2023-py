"""14: PROBLEM NAME"""
from copy import deepcopy
from functools import reduce
from itertools import pairwise
import aoc.util


def contains(interval, value) -> bool:
    return interval[0] <= value and value <= interval[1]


class Dish:
    def __init__(self, input):
        self.row_intervals = []
        self.col_intervals = []
        lines = input.splitlines()
        height = len(lines)
        width = len(lines[0])
        self.rounds_in_cols = []
        self.rounds_in_rows = []
        col_interval_markers = []
        for i in range(0, width):
            col_interval_markers.append([-1])
            self.rounds_in_cols.append([])

        for row, line in enumerate(lines):
            self.rounds_in_rows.append([])
            interval_markers = [-1]
            for col, ch in enumerate(line):
                if ch == '#':
                    col_interval_markers[col].append(row)
                    interval_markers.append(col)
                elif ch == 'O':
                    self.rounds_in_cols[col].append(row)

            interval_markers.append(width)

            intervals = []
            for start, end in pairwise(interval_markers):
                if end - start < 2:
                    continue
                intervals.append((start + 1, end - 1))

            self.row_intervals.append((len(self.row_intervals), intervals))

        for col_markers in col_interval_markers:
            col_markers.append(height)
            intervals = []
            for start, end in pairwise(col_markers):
                if end - start < 2:
                    continue
                intervals.append((start + 1, end - 1))
            self.col_intervals.append((len(self.col_intervals), intervals))

    def total_load_p1(self) -> int:
        height = len(self.rounds_in_rows)
        return sum(len(r) * (height - i) for i, r in enumerate(self.rounds_in_rows))

    def cycle(self, count) -> int:
        cache = {}
        loads = []

        for cycle_idx in range(0, count):
            self.tilt_north()
            self.tilt_west()
            self.tilt_south()
            load = self.tilt_east()

            if cycle_idx > 4:
                key = load << 96 | loads[-1] << 64 | loads[-2] << 32 | loads[-3]
                if key in cache:
                    e = cache[key]
                    if e != cycle_idx:
                        period = cycle_idx - e
                        rem = (count - cycle_idx) % period
                        return loads[e + rem - 1]

                cache[key] = cycle_idx

            loads.append(load)

    def tilt_north(self):
        for col, intervals in self.col_intervals:
            interval_idx = 0
            interval_insert_count = 0

            for value in self.rounds_in_cols[col]:
                while not contains(intervals[interval_idx], value):
                    interval_idx += 1
                    interval_insert_count = 0

                new_value = intervals[interval_idx][0] + interval_insert_count
                self.rounds_in_rows[new_value].append(col)
                interval_insert_count += 1

            self.rounds_in_cols[col].clear()

    def tilt_south(self):
        for col, intervals in self.col_intervals:
            interval_idx = 0
            interval_insert_count = 0

            for value in self.rounds_in_cols[col]:
                while not contains(intervals[interval_idx], value):
                    interval_idx += 1
                    interval_insert_count = 0

                new_value = intervals[interval_idx][1] - interval_insert_count
                self.rounds_in_rows[new_value].append(col)
                interval_insert_count += 1

            self.rounds_in_cols[col].clear()

    def tilt_west(self):
        for row, intervals in self.row_intervals:
            interval_idx = 0
            interval_insert_count = 0

            for value in self.rounds_in_rows[row]:
                while not contains(intervals[interval_idx], value):
                    interval_idx += 1
                    interval_insert_count = 0

                new_value = intervals[interval_idx][0] + interval_insert_count
                self.rounds_in_cols[new_value].append(row)
                interval_insert_count += 1

            self.rounds_in_rows[row].clear()

    def tilt_east(self) -> int:
        load = 0
        height = len(self.rounds_in_rows)
        for row, intervals in self.row_intervals:
            interval_idx = 0
            interval_insert_count = 0
            load += (height - row) * len(self.rounds_in_rows[row])
            for value in self.rounds_in_rows[row]:
                while not contains(intervals[interval_idx], value):
                    interval_idx += 1
                    interval_insert_count = 0

                new_value = intervals[interval_idx][1] - interval_insert_count
                self.rounds_in_cols[new_value].append(row)
                interval_insert_count += 1

            self.rounds_in_rows[row].clear()

        return load


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.dish = Dish(input)

    def part_one(self) -> int:
        dish = deepcopy(self.dish)
        dish.tilt_north()
        return dish.total_load_p1()

    def part_two(self) -> int:
        return self.dish.cycle(1000000000)

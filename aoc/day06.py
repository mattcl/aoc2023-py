"""06: PROBLEM NAME"""
import math

import aoc.util


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)
        lines = input.splitlines()
        times = lines[0].replace("Time:", "")
        records = lines[1].replace("Distance:", "")
        self.times = list(map(int, times.split()))
        self.records = list(map(int, records.split()))

        self.big_time = int(times.replace(" ", ""))
        self.big_record = int(records.replace(" ", ""))

    def ways_to_beat(self, time, record):
        t2 = time * time
        b = math.sqrt(t2 - 4.0 * record)

        lower_raw = 0.5 * (time - b)
        upper_raw = 0.5 * (time + b)

        lower = math.ceil(lower_raw)
        upper = math.floor(upper_raw)

        while (time - lower) * lower <= record:
            lower += 1

        while (time - upper) * upper <= record:
            upper -= 1

        return upper - lower + 1

    def part_one(self) -> int:
        prod = 1

        for i in range(0, len(self.times)):
            prod *= self.ways_to_beat(self.times[i], self.records[i])

        return prod

    def part_two(self) -> int:
        return self.ways_to_beat(self.big_time, self.big_record)

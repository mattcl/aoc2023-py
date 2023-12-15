"""15: PROBLEM NAME"""
from functools import reduce
from collections import OrderedDict

import aoc.util


def compute_hash(s) -> int:
    return reduce(lambda acc, x: ((acc + ord(x)) * 17) % 256, s, 0)


def sum_bucket(b) -> int:
    return sum(map(lambda item: (item[0] + 1) * item[1][1], enumerate(b.items())))


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)
        buckets = list(map(lambda _: OrderedDict(), range(0, 256)))
        self.p1 = 0
        for step in input.strip().split(','):
            self.p1 += compute_hash(step)
            parts = step.split('=')
            if len(parts) == 1:
                # we're removing
                label = step[:-1]
                key = compute_hash(label)

                if label in buckets[key]:
                    del buckets[key][label]

            else:
                # we're inserting
                key = compute_hash(parts[0])
                value = int(parts[1])

                buckets[key][parts[0]] = value

        self.p2 = sum(map(lambda item: (item[0] + 1) * sum_bucket(item[1]), enumerate(buckets)))

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2

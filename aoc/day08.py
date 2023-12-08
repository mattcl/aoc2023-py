"""08: PROBLEM NAME"""
from functools import reduce
import itertools
import math

import aoc.util


class Node:
    def __init__(self, key, left, right):
        self.left = left
        self.right = right
        self.ends_with_a = key.endswith("A")
        self.ends_with_z = key.endswith("Z")


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)
        parts = input.split("\n\n")
        self.instructions = parts[0]
        self.mapping = {}
        for line in parts[1].splitlines():
            components = line.split(" = ")
            key = components[0]
            sides = components[1].replace("(", "").replace(")", "").split(", ")
            self.mapping[key] = Node(key, sides[0], sides[1])

    def part_one(self) -> int:
        count = 0
        cur = "AAA"
        cur_node = self.mapping[cur]

        for i in itertools.cycle(self.instructions):
            if cur == "ZZZ":
                return count

            if i == "L":
                cur = cur_node.left
            else:
                cur = cur_node.right

            cur_node = self.mapping[cur]
            count += 1

        # should be impossible to get here
        return -1

    def part_two(self) -> int:
        starting = (self.get_first_z(x) for x, y in self.mapping.items() if y.ends_with_a)
        return math.lcm(*starting)

    def get_first_z(self, start):
        count = 0
        cur = start
        cur_node = self.mapping[cur]

        for i in itertools.cycle(self.instructions):
            if cur_node.ends_with_z:
                return count

            if i == "L":
                cur = cur_node.left
            else:
                cur = cur_node.right

            cur_node = self.mapping[cur]
            count += 1

        # should be impossible to get here
        return -1

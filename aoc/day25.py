"""25: PROBLEM NAME"""
from itertools import combinations
import random

import networkx as nx

import aoc.util


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.graph = nx.Graph()

        for line in input.splitlines():
            parts = line.split()
            name = parts[0][:-1]

            for n in parts[1:]:
                self.graph.add_edge(name, n, capacity=1)

    def part_one(self) -> int:
        graph_nodes = list(self.graph.nodes())

        while True:
            # we have a 50% chance of picking two nodes in opposite sides of
            # the graph, I think...
            first, second = random.sample(graph_nodes, 2)
            if first == second:
                continue

            cut, partitions = nx.minimum_cut(self.graph, first, second)

            if cut == 3:
                return len(partitions[0]) * len(partitions[1])

    def part_two(self) -> str:
        return "no part two"

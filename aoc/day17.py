"""17: PROBLEM NAME"""
from collections import defaultdict

import aoc.util


HORIZONTAL = 0
VERTICAL = 1


# we're going to avoid having to consider moving forward by pre-generating all
# the forward locations, if possible
def neighbors(grid, width, height, minimum, maximum, start):
    if start[2] == HORIZONTAL:
        north_cost = 0
        for i in range(1, minimum):
            if start[0] < i:
                break

            north_cost += grid[start[0] - i][start[1]]

        north_max = min(maximum, start[0])

        south_cost = 0
        for i in range(1, minimum):
            if start[0] + i >= height:
                break

            south_cost += grid[start[0] + i][start[1]]

        south_max = min(maximum, height - 1 - start[0])

        out = []
        if north_max >= minimum:
            for i in range(minimum, north_max + 1):
                new_row = start[0] - i
                north_cost += grid[new_row][start[1]]
                out.append(
                    (
                        north_cost,
                        (new_row, start[1], VERTICAL),
                    )
                )

        if south_max >= minimum:
            for i in range(minimum, south_max + 1):
                new_row = start[0] + i
                south_cost += grid[new_row][start[1]]
                out.append(
                    (
                        south_cost,
                        (new_row, start[1], VERTICAL),
                    )
                )

        return out

    # handle vertical
    else:
        west_cost = 0
        for i in range(1, minimum):
            if start[1] < i:
                break

            west_cost += grid[start[0]][start[1] - i]

        west_max = min(maximum, start[1])

        east_cost = 0
        for i in range(1, minimum):
            if start[1] + i >= width:
                break

            east_cost += grid[start[0]][start[1] + i]

        east_max = min(maximum, width - 1 - start[1])

        out = []
        if west_max >= minimum:
            for i in range(minimum, west_max + 1):
                new_col = start[1] - i
                west_cost += grid[start[0]][new_col]
                out.append(
                    (
                        west_cost,
                        (start[0], new_col, HORIZONTAL),
                    )
                )

        if east_max >= minimum:
            for i in range(minimum, east_max + 1):
                new_col = start[1] + i
                east_cost += grid[start[0]][new_col]
                out.append(
                    (
                        east_cost,
                        (start[0], new_col, HORIZONTAL),
                    )
                )

        return out


class BucketQueue:
    def __init__(self):
        self.buckets = [[] for _ in range(1000)]
        self.first = None

    def push(self, cost, value):
        if len(self.buckets) <= cost:
            for _ in range(cost - len(self.buckets) + 1):
                self.buckets.append(list())

        self.buckets[cost].append(value)

        if self.first is None or self.first > cost:
            self.first = cost

    def pop(self):
        if self.first is None:
            return None

        cost = self.first

        v = self.buckets[self.first].pop()

        if len(self.buckets[self.first]) == 0:
            start = self.first + 1
            self.first = None
            for i in range(start, len(self.buckets)):
                if len(self.buckets[i]) > 0:
                    self.first = i
                    break

        return cost, v


def dijkstra(grid, minimum, maximum):
    height = len(grid)
    width = len(grid[0])
    end = (height - 1, width - 1)

    start_horiz = (0, 0, HORIZONTAL)
    start_vert = (0, 0, VERTICAL)

    def default_value():
        return 1000000

    costs = defaultdict(default_value)

    # ndoes in the heap are
    # (row, col, orientation)
    heap = BucketQueue()

    # we're just going to push all the possible starts on the heap to deal with
    # the special first square
    for neighbor_cost, neighbor in neighbors(grid, width, height, minimum, maximum, start_horiz):
        costs[neighbor] = neighbor_cost
        heap.push(neighbor_cost, neighbor)

    for neighbor_cost, neighbor in neighbors(grid, width, height, minimum, maximum, start_vert):
        costs[neighbor] = neighbor_cost
        heap.push(neighbor_cost, neighbor)

    # now find the path
    while True:
        res = heap.pop()
        if res is None:
            break

        cur_cost, node = res

        if node[0] == end[0] and node[1] == end[1]:
            return cur_cost

        if cur_cost > costs[node]:
            continue

        for neighbor_cost, neighbor in neighbors(grid, width, height, minimum, maximum, node):
            next_cost = cur_cost + neighbor_cost

            if next_cost < costs[neighbor]:
                costs[neighbor] = next_cost
                heap.push(next_cost, neighbor)


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.grid = list(list(map(int, line)) for line in input.splitlines())

    def part_one(self) -> int:
        return dijkstra(self.grid, 1, 3)

    def part_two(self) -> int:
        return dijkstra(self.grid, 4, 10)

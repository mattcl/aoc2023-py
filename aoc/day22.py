"""22: PROBLEM NAME"""
from collections import defaultdict, deque
from multiprocessing import Pool


import aoc.util


def set_z(cube, z):
    delta = z - cube[0][2]
    cube[0][2] += delta
    cube[1][2] += delta


def pool_init(a, b):
    global above
    global below
    above = a
    below = b


def search(start) -> int:
    global above
    global below
    generation = deque()
    generation.append(start)
    removed = set()
    removed.add(start)

    while len(generation) > 0:
        next = deque()
        for i in generation:
            for n in above[i]:
                if n in removed:
                    continue

                if all(b in removed for b in below[n]):
                    removed.add(n)
                    next.append(n)

        generation = next

    return len(removed) - 1


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.cubes = []
        for line in input.splitlines():
            start_components, end_components = line.split('~')
            start = list(map(int, start_components.split(',')))
            end = list(map(int, end_components.split(',')))
            # (start, end)
            self.cubes.append([start, end])

        self.cubes.sort(key=lambda x: x[0][2])

    def part_one(self) -> int:
        max_x = 0
        max_y = 0

        for cube in self.cubes:
            if cube[0][0] > max_x:
                max_x = cube[0][0]

            if cube[1][0] > max_x:
                max_x = cube[1][0]

            if cube[0][1] > max_y:
                max_y = cube[0][1]

            if cube[1][1] > max_y:
                max_y = cube[1][1]

        topology = [[-1 for _ in range(max_x + 2)] for _ in range(max_y + 2)]

        self.above = defaultdict(list)
        self.below = defaultdict(list)

        self.required = set()

        for i in range(len(self.cubes)):
            brick = self.cubes[i]

            highest = 0
            highest_idxs = []

            sx = min(brick[0][0], brick[1][0])
            ex = max(brick[0][0], brick[1][0]) + 1
            sy = min(brick[0][1], brick[1][1])
            ey = max(brick[0][1], brick[1][1]) + 1

            for x in range(sx, ex):
                for y in range(sy, ey):
                    idx = topology[y][x]

                    if idx != -1 and self.cubes[idx][1][2] >= highest:
                        if self.cubes[idx][1][2] > highest:
                            highest_idxs.clear()
                            highest = self.cubes[idx][1][2]

                        if len(highest_idxs) == 0 or highest_idxs[-1] != idx:
                            highest_idxs.append(idx)

                    topology[y][x] = i

            if len(highest_idxs) == 1:
                self.required.add(highest_idxs[0])

            for idx in highest_idxs:
                self.above[idx].append(i)
                self.below[i].append(idx)

            set_z(self.cubes[i], highest + 1)

        return len(self.cubes) - len(self.required)

    def part_two(self) -> int:
        with Pool(initializer=pool_init, initargs=[self.above, self.below]) as pool:
            return sum(pool.map(search, self.required))

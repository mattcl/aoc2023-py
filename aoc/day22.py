"""22: PROBLEM NAME"""
from collections import defaultdict, deque
from multiprocessing import Pool


import aoc.util


def rect_intersection(this, other) -> bool:
    begin_x = max(this[0], other[0])
    end_x = min(this[2], other[2])

    if begin_x > end_x:
        return False

    begin_y = max(this[1], other[1])
    end_y = min(this[3], other[3])

    return begin_y <= end_y


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

    while len(generation) > 0:
        next = deque()
        for i in generation:
            removed.add(i)

        for i in generation:
            for n in above[i]:
                if all(b in removed for b in below[n]):
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
            # (x0, y0, x1, y1)
            xy_rect = (
                min(start[0], end[0]),
                min(start[1], end[1]),
                max(start[0], end[0]),
                max(start[1], end[1]),
            )
            # (start, end, xy_rect)
            self.cubes.append([start, end, xy_rect])

        self.cubes.sort(key=lambda x: x[0][2])

    def part_one(self) -> int:
        # [z_height, index]
        stable_bricks = []
        self.above = defaultdict(list)
        self.below = defaultdict(list)
        for i in range(len(self.cubes)):
            brick = self.cubes[i]

            if brick[0][2] > 1:
                stable_bricks.sort()
                max_height = -1
                for (entry_z, entry_idx) in reversed(stable_bricks):
                    next_z = entry_z + 1
                    cur_b = self.cubes[entry_idx][2]

                    if next_z >= max_height:
                        if rect_intersection(cur_b, brick[2]):
                            if max_height == -1:
                                max_height = next_z

                            self.above[entry_idx].append(i)
                            self.below[i].append(entry_idx)
                    else:
                        break

                if max_height == -1:
                    set_z(self.cubes[i], 1)
                else:
                    set_z(self.cubes[i], max_height)

            stable_bricks.append((self.cubes[i][1][2], i))

        self.required = set((x[0] for x in self.below.values() if len(x) == 1))

        return len(self.cubes) - len(self.required)

    def part_two(self) -> int:
        with Pool(initializer=pool_init, initargs=[self.above, self.below]) as pool:
            return sum(pool.map(search, self.required))

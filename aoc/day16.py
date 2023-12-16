"""16: PROBLEM NAME"""
from multiprocessing import Pool
from collections import deque, defaultdict

import aoc.util


NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3

OPPOSITE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}


def propagate(start):
    global grid
    global width
    global height
    seen = defaultdict(set)
    beams = deque([start])

    while len(beams) > 0:
        loc, dir = beams.pop()
        tile = grid[loc[0]][loc[1]]

        if loc in seen:
            if dir in seen[loc]:
                continue

            if tile == '.' and OPPOSITE[dir] in seen[loc]:
                continue

        seen[loc].add(dir)

        match dir:
            case 0:
                match tile:
                    case '/':
                        new_pos = loc[1] + 1
                        if new_pos < width:
                            beams.append(((loc[0], new_pos), EAST))
                    case '\\':
                        new_pos = loc[1] - 1
                        if new_pos >= 0:
                            beams.append(((loc[0], new_pos), WEST))
                    case '-':
                        new_pos = loc[1] - 1
                        if new_pos >= 0:
                            beams.append(((loc[0], new_pos), WEST))

                        new_pos = loc[1] + 1
                        if new_pos < width:
                            beams.append(((loc[0], new_pos), EAST))
                    case _:
                        if loc[0] > 0:
                            beams.append(((loc[0] - 1, loc[1]), dir))
            case 2:
                match tile:
                    case '/':
                        new_pos = loc[1] - 1
                        if new_pos >= 0:
                            beams.append(((loc[0], new_pos), WEST))
                    case '\\':
                        new_pos = loc[1] + 1
                        if new_pos < width:
                            beams.append(((loc[0], new_pos), EAST))
                    case '-':
                        new_pos = loc[1] - 1
                        if new_pos >= 0:
                            beams.append(((loc[0], new_pos), WEST))

                        new_pos = loc[1] + 1
                        if new_pos < width:
                            beams.append(((loc[0], new_pos), EAST))
                    case _:
                        if loc[0] < height - 1:
                            beams.append(((loc[0] + 1, loc[1]), dir))
            case 3:
                match tile:
                    case '/':
                        new_pos = loc[0] - 1
                        if new_pos >= 0:
                            beams.append(((new_pos, loc[1]), NORTH))
                    case '\\':
                        new_pos = loc[0] + 1
                        if new_pos < height:
                            beams.append(((new_pos, loc[1]), SOUTH))
                    case '|':
                        new_pos = loc[0] - 1
                        if new_pos >= 0:
                            beams.append(((new_pos, loc[1]), NORTH))

                        new_pos = loc[0] + 1
                        if new_pos < height:
                            beams.append(((new_pos, loc[1]), SOUTH))
                    case _:
                        if loc[1] < width - 1:
                            beams.append(((loc[0], loc[1] + 1), dir))
            case 1:
                match tile:
                    case '/':
                        new_pos = loc[0] + 1
                        if new_pos < height:
                            beams.append(((new_pos, loc[1]), SOUTH))
                    case '\\':
                        new_pos = loc[0] - 1
                        if new_pos >= 0:
                            beams.append(((new_pos, loc[1]), NORTH))
                    case '|':
                        new_pos = loc[0] - 1
                        if new_pos >= 0:
                            beams.append(((new_pos, loc[1]), NORTH))

                        new_pos = loc[0] + 1
                        if new_pos < height:
                            beams.append(((new_pos, loc[1]), SOUTH))
                    case _:
                        if loc[1] > 0:
                            beams.append(((loc[0], loc[1] - 1), dir))

    return len(seen)


def pool_init(shared_grid):
    global grid
    global width
    global height
    grid = shared_grid
    width = len(shared_grid[0])
    height = len(shared_grid)


def propagate_all(grid, width, height):
    bot = height - 1
    right = width - 1
    starts = deque()
    for i in range(0, height):
        starts.append(((i, 0), EAST))
        starts.append(((i, right), WEST))

    for i in range(0, width):
        starts.append(((0, i), SOUTH))
        starts.append(((bot, i), NORTH))

    with Pool(initializer=pool_init, initargs=[grid]) as pool:
        return pool.map(propagate, starts)


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        grid = input.splitlines()
        height = len(grid)
        width = len(grid[0])

        vals = propagate_all(grid, width, height)
        self.p1 = vals[0]
        self.p2 = max(vals)

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2

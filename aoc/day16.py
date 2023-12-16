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

MIRROR_F = {
    NORTH: EAST,
    SOUTH: WEST,
    EAST: NORTH,
    WEST: SOUTH,
}

MIRROR_B = {
    NORTH: WEST,
    SOUTH: EAST,
    EAST: SOUTH,
    WEST: NORTH,
}

LOCATION_OFFSET = {
    NORTH: (-1, 0),
    SOUTH: (1, 0),
    EAST: (0, 1),
    WEST: (0, -1),
}


def next_location(location, dir, width, height):
    match dir:
        case 0:
            if location[0] > 0:
                return (location[0] - 1, location[1])
        case 2:
            if location[0] < height - 1:
                return (location[0] + 1, location[1])
        case 3:
            if location[1] < width - 1:
                return (location[0], location[1] + 1)
        case 1:
            if location[1] > 0:
                return (location[0], location[1] - 1)

    return None


def propagate(start):
    global grid
    global width
    global height
    seen = defaultdict(set)
    beams = deque([start])

    while len(beams) > 0:
        beam = beams.pop()
        tile = grid[beam[0][0]][beam[0][1]]

        if beam[0] in seen:
            if beam[1] in seen[beam[0]]:
                continue

            if tile == '.' and OPPOSITE[beam[1]] in seen[beam[0]]:
                continue

        seen[beam[0]].add(beam[1])

        match tile:
            case '/':
                next_dir = MIRROR_F[beam[1]]
                next = next_location(beam[0], next_dir, width, height)
                if next is not None:
                    beams.append((next, next_dir))
            case '\\':
                next_dir = MIRROR_B[beam[1]]
                next = next_location(beam[0], next_dir, width, height)
                if next is not None:
                    beams.append((next, next_dir))
            case '|':
                if beam[1] == EAST or beam[1] == WEST:
                    next = next_location(beam[0], NORTH, width, height)
                    if next is not None:
                        beams.append((next, NORTH))

                    next = next_location(beam[0], SOUTH, width, height)
                    if next is not None:
                        beams.append((next, SOUTH))

                else:
                    next = next_location(beam[0], beam[1], width, height)
                    if next is not None:
                        beams.append((next, beam[1]))

            case '-':
                if beam[1] == NORTH or beam[1] == SOUTH:
                    next = next_location(beam[0], EAST, width, height)
                    if next is not None:
                        beams.append((next, EAST))

                    next = next_location(beam[0], WEST, width, height)
                    if next is not None:
                        beams.append((next, WEST))

                else:
                    next = next_location(beam[0], beam[1], width, height)
                    if next is not None:
                        beams.append((next, beam[1]))
            case _:
                next = next_location(beam[0], beam[1], width, height)
                if next is not None:
                    beams.append((next, beam[1]))

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

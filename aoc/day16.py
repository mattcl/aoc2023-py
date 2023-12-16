"""16: PROBLEM NAME"""
from multiprocessing import Pool
from collections import deque

import aoc.util


NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3

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


def propagate(grid, start):
    height = len(grid)
    width = len(grid[0])
    seen = set()
    energized = set()
    beams = deque([start])

    while len(beams) > 0:
        beam = beams.pop()

        if beam in seen:
            continue

        seen.add(beam)
        energized.add(beam[0])

        match grid[beam[0][0]][beam[0][1]]:
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

    return len(energized)


def propagate_all(grid):
    height = len(grid)
    width = len(grid[0])
    bot = height - 1
    right = width - 1
    starts = []
    for i in range(0, height):
        starts.append([
            grid,
            ((i, 0), EAST)
        ])
        starts.append([
            grid,
            ((i, right), WEST)
        ])

    for i in range(0, width):
        starts.append([
            grid,
            ((0, i), SOUTH)
        ])
        starts.append([
            grid,
            ((bot, i), NORTH)
        ])

    with Pool() as pool:
        return pool.starmap(propagate, starts)


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        grid = input.splitlines()
        start = ((0, 0), EAST)
        vals = propagate_all(grid)
        self.p1 = vals[0]
        self.p2 = max(vals)

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2

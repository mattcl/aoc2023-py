"""10: pipe maze"""
from enum import Enum
import aoc.util


class Directions(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Location:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def add(self, other):
        return Location(self.row + other.row, self.col + other.col)

    def __eq__(self, other):
        return isinstance(other, Location) and self.row == other.row and self.col == other.col

    # this is a much dumber version than the one in my rust solution
    def tile_between(self, other, start):
        if self.row == other.row:
            return HORIZONAL
        elif self.col == other.col:
            return VERTICAL
        elif self.col < other.col and self.row < other.row:
            return SW90
        elif self.col > other.col and self.row > other.row:
            return NE90
        elif self.col < other.col and self.row > other.row:
            if self.row == start.row:
                return NW90
            elif self.col == start.col:
                return SE90

        assert False, "should have been unreachable"


NEIGHBORS = [
    Location(-1, 0),
    Location(0, 1),
    Location(1, 0),
    Location(0, -1),
]


VERTICAL = 0
HORIZONAL = 1
NE90 = 2
NW90 = 3
SW90 = 4
SE90 = 5
GROUND = 6
START = 7


TRANSLATE = {
    '|': VERTICAL,
    '-': HORIZONAL,
    'L': NE90,
    'J': NW90,
    '7': SW90,
    'F': SE90,
    '.': GROUND,
    'S': START,
}


class Actor:
    def __init__(self, location, facing, tile):
        self.location = location
        self.facing = facing
        self.tile = tile
        self.right_turns = 0
        self.left_turns = 0

    def shoelace_right(self):
        if self.tile == VERTICAL:
            if self.facing == Directions.SOUTH:
                return self.location.col - 1
            else:
                return -self.location.col
        elif self.tile == NW90 and self.facing == Directions.NORTH:
            return -self.location.col
        elif self.tile == SW90 and self.facing == Directions.WEST:
            return -self.location.col
        elif self.tile == NE90 and self.facing == Directions.EAST:
            return self.location.col - 1
        elif self.tile == SE90 and self.facing == Directions.SOUTH:
            return self.location.col - 1
        else:
            return 0

    def shoelace_left(self):
        if self.tile == VERTICAL:
            if self.facing == Directions.NORTH:
                return self.location.col - 1
            else:
                return -self.location.col
        elif self.tile == NW90 and self.facing == Directions.WEST:
            return -self.location.col
        elif self.tile == SW90 and self.facing == Directions.SOUTH:
            return -self.location.col
        elif self.tile == NE90 and self.facing == Directions.NORTH:
            return self.location.col - 1
        elif self.tile == SE90 and self.facing == Directions.EAST:
            return self.location.col - 1
        else:
            return 0

    def advance(self, grid):
        next_location = self.location.add(NEIGHBORS[self.facing.value])

        tile = grid[next_location.row][next_location.col]

        if self.facing == Directions.NORTH:
            if tile == SW90:
                self.facing = Directions.WEST
                self.left_turns += 1
            elif tile == SE90:
                self.facing = Directions.EAST
                self.right_turns += 1
        elif self.facing == Directions.SOUTH:
            if tile == NE90:
                self.facing = Directions.EAST
                self.left_turns += 1
            elif tile == NW90:
                self.facing = Directions.WEST
                self.right_turns += 1
        elif self.facing == Directions.EAST:
            if tile == SW90:
                self.facing = Directions.SOUTH
                self.right_turns += 1
            elif tile == NW90:
                self.facing = Directions.NORTH
                self.left_turns += 1
        elif self.facing == Directions.WEST:
            if tile == SE90:
                self.facing = Directions.SOUTH
                self.left_turns += 1
            elif tile == NE90:
                self.facing = Directions.NORTH
                self.right_turns += 1

        self.location = next_location
        self.tile = tile


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.grid = []
        self.start = None
        for row, line in enumerate(input.splitlines()):
            if self.start is None:
                col = line.find('S')
                if col >= 0:
                    self.start = Location(row, col)
            self.grid.append([TRANSLATE[ch] for ch in line])

        self.height = len(self.grid)
        self.width = len(self.grid[0])

        steps = 1
        actor = self.determine_starting_actor()
        shoelace_right = actor.shoelace_right()
        shoelace_left = actor.shoelace_left()

        while not actor.location == self.start:
            steps += 1
            actor.advance(self.grid)
            shoelace_right += actor.shoelace_right()
            shoelace_left += actor.shoelace_left()

        # if we have more right turns than left turns, the tiles in the loop are
        # to our right, otherwise, they're to our left
        if actor.right_turns > actor.left_turns:
            self.num_inside = shoelace_right
        else:
            self.num_inside = shoelace_left

        self.steps = steps // 2

    def determine_starting_actor(self):
        # determine a position off of the starting location to move from
        dirs = [Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST]
        actors = []
        for dir in dirs:
            loc = self.start.add(NEIGHBORS[dir.value])
            if loc.row >= 0 and loc.col >= 0 and loc.row < self.height and loc.col < self.width:
                tile = self.grid[loc.row][loc.col]
                if tile == VERTICAL and (dir == Directions.NORTH or dir == Directions.SOUTH):
                    actors.append(Actor(loc, dir, tile))

                if tile == HORIZONAL and (dir == Directions.WEST or dir == Directions.EAST):
                    actors.append(Actor(loc, dir, tile))

                if tile == SW90 and dir == Directions.NORTH:
                    actors.append(Actor(loc, Directions.WEST, tile))

                if tile == SE90 and dir == Directions.NORTH:
                    actors.append(Actor(loc, Directions.EAST, tile))

                if tile == NW90 and dir == Directions.SOUTH:
                    actors.append(Actor(loc, Directions.WEST, tile))

                if tile == NE90 and dir == Directions.SOUTH:
                    actors.append(Actor(loc, Directions.EAST, tile))

                if tile == SW90 and dir == Directions.EAST:
                    actors.append(Actor(loc, Directions.SOUTH, tile))

                if tile == NW90 and dir == Directions.EAST:
                    actors.append(Actor(loc, Directions.NORTH, tile))

                if tile == SE90 and dir == Directions.WEST:
                    actors.append(Actor(loc, Directions.SOUTH, tile))

                if tile == NE90 and dir == Directions.WEST:
                    actors.append(Actor(loc, Directions.NORTH, tile))

        start_tile = actors[1].location.tile_between(actors[0].location, self.start)
        self.grid[self.start.row][self.start.col] = start_tile

        return actors[0]

    def part_one(self) -> int:
        return self.steps

    def part_two(self) -> int:
        return self.num_inside

"""10: pipe maze"""
from enum import Enum
import aoc.util


class Directions(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def right(self):
        match self:
            case Directions.NORTH:
                return Directions.EAST
            case Directions.EAST:
                return Directions.SOUTH
            case Directions.SOUTH:
                return Directions.WEST
            case Directions.WEST:
                return Directions.NORTH

    def left(self):
        match self:
            case Directions.NORTH:
                return Directions.WEST
            case Directions.WEST:
                return Directions.SOUTH
            case Directions.SOUTH:
                return Directions.EAST
            case Directions.EAST:
                return Directions.NORTH


class Location:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def add(self, other):
        return Location(self.row + other.row, self.col + other.col)

    def __eq__(self, other):
        return isinstance(other, Location) and self.row == other.row and self.col == other.col


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
PROCESSED = 8


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


class State:
    def __init__(self, location, facing, tile):
        self.location = location
        self.facing = facing
        self.tile = tile

    def right_locs(self, maze, width, height):
        out = []
        if self.tile == NW90 and self.facing == Directions.NORTH:
            loc = self.location.add(NEIGHBORS[Directions.SOUTH.value])
            if maze[loc.row][loc.col] != PROCESSED:
                out.append(loc)
        elif self.tile == SE90 and self.facing == Directions.SOUTH:
            loc = self.location.add(NEIGHBORS[Directions.NORTH.value])
            if maze[loc.row][loc.col] != PROCESSED:
                out.append(loc)
        elif self.tile == NE90 and self.facing == Directions.EAST:
            loc = self.location.add(NEIGHBORS[Directions.WEST.value])
            if maze[loc.row][loc.col] != PROCESSED:
                out.append(loc)
        elif self.tile == SW90 and self.facing == Directions.WEST:
            loc = self.location.add(NEIGHBORS[Directions.EAST.value])
            if maze[loc.row][loc.col] != PROCESSED:
                out.append(loc)

        loc = self.location.add(NEIGHBORS[self.facing.right().value])
        if maze[loc.row][loc.col] != PROCESSED:
            out.append(loc)

        return out

    def left_locs(self, maze, width, height):
        out = []
        if self.tile == NE90 and self.facing == Directions.NORTH:
            loc = self.location.add(NEIGHBORS[Directions.SOUTH.value])
            if maze[loc.row][loc.col] != PROCESSED:
                out.append(loc)
        elif self.tile == SW90 and self.facing == Directions.SOUTH:
            loc = self.location.add(NEIGHBORS[Directions.NORTH.value])
            if maze[loc.row][loc.col] != PROCESSED:
                out.append(loc)
        elif self.tile == SE90 and self.facing == Directions.EAST:
            loc = self.location.add(NEIGHBORS[Directions.WEST.value])
            if maze[loc.row][loc.col] != PROCESSED:
                out.append(loc)
        elif self.tile == NW90 and self.facing == Directions.WEST:
            loc = self.location.add(NEIGHBORS[Directions.EAST.value])
            if maze[loc.row][loc.col] != PROCESSED:
                out.append(loc)

        loc = self.location.add(NEIGHBORS[self.facing.left().value])
        if maze[loc.row][loc.col] != PROCESSED:
            out.append(loc)

        return out



class Actor:
    def __init__(self, location, facing, tile):
        self.location = location
        self.facing = facing
        self.right_turns = 0
        self.left_turns = 0
        self.history = [State(location, facing, tile)]

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

        self.history.append(State(self.location, self.facing, tile))


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
        self.grid[self.start.row][self.start.col] = PROCESSED
        self.grid[actor.location.row][actor.location.col] = PROCESSED

        while not actor.location == self.start:
            steps += 1
            actor.advance(self.grid)
            self.grid[actor.location.row][actor.location.col] = PROCESSED

        self.num_inside = 0
        # if we have more right turns than left turns, the tiles in the loop are
        # to our right, otherwise, they're to our left
        if actor.right_turns > actor.left_turns:
            for state in actor.history:
                locs = state.right_locs(self.grid, self.width, self.height)

                if len(locs) > 0:
                    self.flood(locs)
        else:
            for state in actor.history:
                locs = state.left_locs(self.grid, self.width, self.height)

                if len(locs) > 0:
                    self.flood(locs)

        self.steps = steps // 2

    def determine_starting_actor(self):
        # determine a position off of the starting location to move from
        dirs = [Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST]
        for dir in dirs:
            loc = self.start.add(NEIGHBORS[dir.value])
            if loc.row >= 0 and loc.col >= 0 and loc.row < self.height and loc.col < self.width:
                tile = self.grid[loc.row][loc.col]
                if tile == VERTICAL and (dir == Directions.NORTH or dir == Directions.SOUTH):
                    return Actor(loc, dir, tile)

                if tile == HORIZONAL and (dir == Directions.WEST or dir == Directions.EAST):
                    return Actor(loc, dir, tile)

                if tile == SW90 and dir == Directions.NORTH:
                    return Actor(loc, Directions.WEST, tile)

                if tile == SE90 and dir == Directions.NORTH:
                    return Actor(loc, Directions.EAST, tile)

                if tile == NW90 and dir == Directions.SOUTH:
                    return Actor(loc, Directions.WEST, tile)

                if tile == NE90 and dir == Directions.SOUTH:
                    return Actor(loc, Directions.EAST, tile)

                if tile == SW90 and dir == Directions.EAST:
                    return Actor(loc, Directions.SOUTH, tile)

                if tile == NW90 and dir == Directions.EAST:
                    return Actor(loc, Directions.NORTH, tile)

                if tile == SE90 and dir == Directions.WEST:
                    return Actor(loc, Directions.SOUTH, tile)

                if tile == NE90 and dir == Directions.WEST:
                    return Actor(loc, Directions.NORTH, tile)

    def flood(self, cur):
        next = []
        for cur_loc in cur:
            if self.grid[cur_loc.row][cur_loc.col] == PROCESSED:
                continue
            self.grid[cur_loc.row][cur_loc.col] = PROCESSED
            self.num_inside += 1

            for neighbor in NEIGHBORS:
                loc = cur_loc.add(neighbor)
                if self.grid[loc.row][loc.col] != PROCESSED:
                    next.append(loc)

        if len(next) > 0:
            self.flood(next)

    def part_one(self) -> int:
        return self.steps

    def part_two(self) -> int:
        return self.num_inside

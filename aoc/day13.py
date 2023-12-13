"""13: PROBLEM NAME"""
import aoc.util


def horiz_inner(grid, width, height, left_col, right_col, limit):
    num_conflicts = 0
    for row in range(0, height):
        for offset in range(0, limit):
            if grid[row][left_col - offset] != grid[row][right_col + offset]:
                num_conflicts += 1
                if num_conflicts > 1:
                    return num_conflicts

    return num_conflicts


def reflect_horizontal(grid, width, height) -> int:
    symmetry_loc = None
    fix_pos = None
    for left_col in range(0, width - 1):
        right_col = left_col + 1
        limit = min(left_col + 1, width - right_col)
        v = horiz_inner(grid, width, height, left_col, right_col, limit)
        if v == 0:
            symmetry_loc = left_col + 1
        elif v == 1:
            fix_pos = left_col + 1

        if symmetry_loc is not None and fix_pos is not None:
            return symmetry_loc, fix_pos

    if symmetry_loc is None:
        symmetry_loc = 0

    if fix_pos is None:
        fix_pos = 0

    return symmetry_loc, fix_pos


def vert_inner(grid, width, height, top_row, bot_row, limit):
    num_conflicts = 0
    for col in range(0, width):
        for offset in range(0, limit):
            if grid[top_row - offset][col] != grid[bot_row + offset][col]:
                num_conflicts += 1
                if num_conflicts > 1:
                    return num_conflicts

    return num_conflicts


def reflect_vertical(grid, width, height) -> int:
    symmetry_loc = None
    fix_pos = None
    for top_row in range(0, height - 1):
        bot_row = top_row + 1
        limit = min(top_row + 1, height - bot_row)
        v = vert_inner(grid, width, height, top_row, bot_row, limit)
        if v == 0:
            symmetry_loc = (top_row + 1) * 100
        elif v == 1:
            fix_pos = (top_row + 1) * 100

        if symmetry_loc is not None and fix_pos is not None:
            return symmetry_loc, fix_pos

    if symmetry_loc is None:
        symmetry_loc = 0

    if fix_pos is None:
        fix_pos = 0

    return symmetry_loc, fix_pos


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.p1 = 0
        self.p2 = 0

        for group in input.split("\n\n"):
            lines = group.splitlines()

            height = len(lines)
            width = len(lines[0])

            a, c = reflect_horizontal(lines, width, height)
            b, d = reflect_vertical(lines, width, height)

            self.p1 += a + b
            self.p2 += c + d

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2

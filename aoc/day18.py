"""18: Lavaduct Lagoon"""
import aoc.util
from itertools import pairwise


def rough_area(points):
    return abs(sum(a[1] * b[0] - a[0] * b[1] for a, b in pairwise(points))) // 2


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.points = [(0, 0)]
        self.perimeter = 0
        self.hex_points = [(0, 0)]
        self.hex_perimeter = 0

        cur = (0, 0)
        hex_cur = (0, 0)

        for line in input.splitlines():
            parts = line.split(" ")
            amount = int(parts[1])
            match parts[0]:
                case 'R':
                    cur = (cur[0], cur[1] + amount)
                    self.points.append(cur)
                case 'L':
                    cur = (cur[0], cur[1] - amount)
                    self.points.append(cur)
                case 'U':
                    cur = (cur[0] + amount, cur[1])
                    self.points.append(cur)
                case 'D':
                    cur = (cur[0] - amount, cur[1])
                    self.points.append(cur)

            self.perimeter += amount

            hex_dir = parts[2][-2]
            hex_amount = int(parts[2][2:-2], 16)
            match hex_dir:
                case '0':
                    hex_cur = (hex_cur[0], hex_cur[1] + hex_amount)
                    self.hex_points.append(hex_cur)
                case '2':
                    hex_cur = (hex_cur[0], hex_cur[1] - hex_amount)
                    self.hex_points.append(hex_cur)
                case '3':
                    hex_cur = (hex_cur[0] + hex_amount, hex_cur[1])
                    self.hex_points.append(hex_cur)
                case '1':
                    hex_cur = (hex_cur[0] - hex_amount, hex_cur[1])
                    self.hex_points.append(hex_cur)

            self.hex_perimeter += hex_amount

    def part_one(self) -> int:
        area = rough_area(self.points)
        inside = area - self.perimeter // 2 + 1

        return self.perimeter + inside

    def part_two(self) -> int:
        area = rough_area(self.hex_points)
        inside = area - self.hex_perimeter // 2 + 1

        return self.hex_perimeter + inside

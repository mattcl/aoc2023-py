"""24: PROBLEM NAME"""
from itertools import combinations

# I'd prefer not to have this dependency at all
# import numpy as np  # -> numpy precision was a problem
from sympy.matrices import Matrix

import aoc.util


def intersect_location_xy(this, other):
    d = other[1][0] * this[1][1] - this[1][0] * other[1][1]

    if d != 0:
        x1 = this[0][0]
        y1 = this[0][1]
        vx1 = this[1][0]
        vy1 = this[1][1]
        x2 = other[0][0]
        y2 = other[0][1]
        vx2 = other[1][0]
        vy2 = other[1][1]

        s = ((y2 - y1) * vx2 - vy2 * (x2 - x1)) / d
        if s < 0.0:
            return None, None

        t = ((y2 - y1) * vx1 - vy1 * (x2 - x1)) / d
        if t < 0.0:
            return None, None

        x = x1 + s * vx1
        y = y1 + s * vy1

        return x, y
    else:
        return None, None


def cross_matrix(input):
    return Matrix(
        [
            [0, -input[2], input[1]],
            [input[2], 0, -input[0]],
            [-input[1], input[0], 0],
        ],
    )


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.hail = []
        for line in input.splitlines():
            left, right = line.split(" @ ")
            position = list(map(int, left.split(", ")))
            velocity = list(map(int, right.split(", ")))
            self.hail.append([position, velocity])

    def part_one(self) -> int:
        lower = 200000000000000.0
        upper = 400000000000000.0

        count = 0

        for (left, right) in combinations(self.hail, 2):
            x, y = intersect_location_xy(left, right)
            if x is not None:
                if lower <= x and x <= upper and lower <= y and y <= upper:
                    count += 1

        return count

    def part_two(self) -> int:
        h0_p = Matrix(self.hail[0][0])
        h0_v = Matrix(self.hail[0][1])

        h1_p = Matrix(self.hail[1][0])
        h1_v = Matrix(self.hail[1][1])

        h2_p = Matrix(self.hail[2][0])
        h2_v = Matrix(self.hail[2][1])

        top = -h0_p.cross(h0_v) + h1_p.cross(h1_v)
        bot = -h0_p.cross(h0_v) + h2_p.cross(h2_v)

        rhs = Matrix([
            [top[0]],
            [top[1]],
            [top[2]],
            [bot[0]],
            [bot[1]],
            [bot[2]],
        ])

        ul = cross_matrix(h0_v) - cross_matrix(h1_v)
        ll = cross_matrix(h0_v) - cross_matrix(h2_v)
        ur = -cross_matrix(h0_p) + cross_matrix(h1_p)
        lr = -cross_matrix(h0_p) + cross_matrix(h2_p)

        mat = Matrix([
            [ul[0, 0], ul[0, 1], ul[0, 2], ur[0, 0], ur[0, 1], ur[0, 2]],
            [ul[1, 0], ul[1, 1], ul[1, 2], ur[1, 0], ur[1, 1], ur[1, 2]],
            [ul[2, 0], ul[2, 1], ul[2, 2], ur[2, 0], ur[2, 1], ur[2, 2]],
            [ll[0, 0], ll[0, 1], ll[0, 2], lr[0, 0], lr[0, 1], lr[0, 2]],
            [ll[1, 0], ll[1, 1], ll[1, 2], lr[1, 0], lr[1, 1], lr[1, 2]],
            [ll[2, 0], ll[2, 1], ll[2, 2], lr[2, 0], lr[2, 1], lr[2, 2]],
        ])

        # this apparently doesn't have the right precision
        # inv = np.linalg.inv(mat)
        # res = inv @ rhs
        # res = np.linalg.solve(mat, rhs)
        res = mat.LUsolve(rhs)

        return round(res[0, 0]) + round(res[1, 0]) + round(res[2, 0])

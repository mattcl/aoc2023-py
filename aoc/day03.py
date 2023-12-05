"""03: gear ratios"""
import aoc.util


NEIGHBORS = [
    (0, -1),
    (0, 1),
    # order is important
    (-1, 0),
    (-1, 1),
    (-1, -1),
    (1, 0),
    (1, -1),
    (1, 1),
]


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.lines = input.splitlines()
        self.height = len(self.lines)
        self.width = len(self.lines[0])
        self.total_sum = 0
        self.total_prod = 0

        seen = set()

        for row in range(0, self.height):
            for col in range(0, self.width):
                loc = (row, col)
                ch = self.lines[row][col]

                if not (ch.isdigit() or ch == '.'):
                    locs = []

                    idx = 0
                    while idx < 8:
                        offset = NEIGHBORS[idx]

                        new_row = row + offset[0]
                        if new_row < 0 or new_row >= self.height:
                            idx += 1
                            continue

                        new_col = col + offset[1]
                        if new_col < 0 or new_col >= self.width:
                            idx += 1
                            continue

                        neighbor = self.lines[new_row][new_col]
                        if neighbor.isdigit():
                            locs.append((new_row, new_col))
                            # we can skip evaluating some locations if we have
                            # digits in certain places
                            if idx == 2 or idx == 5:
                                idx += 3
                                continue

                        idx += 1

                    if len(locs) > 0:
                        self.process_candidates(locs, seen, ch == "*")

    def process_candidates(self, candidates, seen, is_star):
        count = 0
        sub_prod = 1

        for candidate in candidates:
            if candidate in seen:
                continue

            seen.add(candidate)

            continue_outer = False
            row = candidate[0]

            digits = 1
            # nums = [self.lines[row][candidate[1]]]
            nums = self.lines[row][candidate[1]]

            # walk west
            pos = candidate[1] - 1
            while pos >= 0:
                west = (row, pos)
                if west in seen:
                    continue_outer = True
                    break

                ch = self.lines[row][pos]
                if ch.isdigit():
                    pos -= 1
                    nums = ch + nums
                    seen.add(west)
                    continue

                break

            if continue_outer:
                continue

            # walk east
            pos = candidate[1] + 1
            while pos < self.width:
                east = (row, pos)
                if east in seen:
                    continue_outer = True
                    break

                ch = self.lines[row][pos]
                if ch.isdigit():
                    pos += 1
                    nums += ch
                    seen.add(east)
                    continue

                break

            if continue_outer:
                continue

            number = int(nums)

            self.total_sum += number
            count += 1
            sub_prod *= number

        if is_star and count == 2:
            self.total_prod += sub_prod


    def part_one(self) -> int:
        return self.total_sum

    def part_two(self) -> int:
        return self.total_prod

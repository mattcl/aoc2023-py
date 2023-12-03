"""03: gear ratios"""
import aoc.util


NEIGHBORS = [
    (-1, 0),
    (-1, 1),
    (-1, -1),
    (0, -1),
    (0, 1),
    (1, 0),
    (1, -1),
    (1, 1),
]


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.lines = input.splitlines()
        self.height = len(self.lines)
        self.width = len(self.lines[0])

        self.symbol_map = {}

        for row in range(0, self.height):
            for col in range(0, self.width):
                loc = (row, col)
                ch = self.lines[row][col]

                if not (ch.isdigit() or ch == '.'):
                    if ch not in self.symbol_map:
                        self.symbol_map[ch] = []

                    locs = []

                    for offset in NEIGHBORS:
                        new_row = row + offset[0]
                        if new_row < 0 or new_row >= self.height:
                            continue

                        new_col = col + offset[1]
                        if new_col < 0 or new_col >= self.width:
                            continue

                        neighbor = self.lines[new_row][new_col]
                        if neighbor.isdigit():
                            locs.append((new_row, new_col))

                    if len(locs) > 0:
                        self.symbol_map[ch].append(locs)

    def part_one(self) -> int:
        seen = set()
        total_sum = 0

        for svs in self.symbol_map.values():
            for vs in svs:
                for candidate in vs:
                    continue_outer = False
                    if candidate in seen:
                        continue

                    seen.add(candidate)

                    digits = 1
                    number = int(self.lines[candidate[0]][candidate[1]])

                    # walk west
                    pos = candidate[1] - 1
                    while pos >= 0:
                        west = (candidate[0], pos)
                        if west in seen:
                            continue_outer = True
                            break

                        ch = self.lines[candidate[0]][pos]
                        if ch.isdigit():
                            pos -= 1
                            number += int(ch) * (10 ** digits)
                            digits += 1
                            seen.add(west)
                            continue

                        break

                    if continue_outer:
                        continue

                    # walk east
                    pos = candidate[1] + 1
                    while pos < self.width:
                        east = (candidate[0], pos)
                        if east in seen:
                            continue_outer = True
                            break

                        ch = self.lines[candidate[0]][pos]
                        if ch.isdigit():
                            pos += 1
                            number = number * 10 + int(ch)
                            seen.add(east)
                            continue

                        break

                    if continue_outer:
                        continue

                    total_sum += number

        return total_sum

    def part_two(self) -> int:
        seen = set()
        total_sum = 0

        for vs in self.symbol_map["*"]:
            count = 0
            sub_prod = 1

            for candidate in vs:
                continue_outer = False
                if candidate in seen:
                    continue

                seen.add(candidate)

                digits = 1
                number = int(self.lines[candidate[0]][candidate[1]])

                # walk west
                pos = candidate[1] - 1
                while pos >= 0:
                    west = (candidate[0], pos)
                    if west in seen:
                        continue_outer = True
                        break

                    ch = self.lines[candidate[0]][pos]
                    if ch.isdigit():
                        pos -= 1
                        number += int(ch) * (10 ** digits)
                        digits += 1
                        seen.add(west)
                        continue

                    break

                if continue_outer:
                    continue

                # walk east
                pos = candidate[1] + 1
                while pos < self.width:
                    east = (candidate[0], pos)
                    if east in seen:
                        continue_outer = True
                        break

                    ch = self.lines[candidate[0]][pos]
                    if ch.isdigit():
                        pos += 1
                        number = number * 10 + int(ch)
                        seen.add(east)
                        continue

                    break

                if continue_outer:
                    continue

                sub_prod *= number
                count += 1

                if count > 2:
                    break

            if count == 2:
                total_sum += sub_prod

        return total_sum

"""21: step counter"""
from collections import deque

import aoc.util


NEIGHBORS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


# In translating my rust solution, I couldn't be bothered to make a version
# that also works with the example input, so this is hard-coded for the real one
class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.grid = input.splitlines()
        self.height = len(self.grid)

    def part_one(self) -> int:
        steps = 64
        parity = steps % 2 == 0
        start = (65, 65)
        seen = set()
        cur = deque()
        cur.append(start)
        seen.add(start)

        count = 1 if parity else 0

        for step in range(1, steps + 1):
            next = deque()
            for loc in cur:
                for dr, dc in NEIGHBORS:
                    next_loc = (loc[0] + dr, loc[1] + dc)
                    if self.grid[next_loc[0]][next_loc[1]] == '#':
                        continue

                    if next_loc not in seen:
                        seen.add(next_loc)
                        if (step % 2 == 0) == parity:
                            count += 1

                        next.append(next_loc)

            cur = next

        return count

    def part_two(self) -> int:
        steps = 26501365
        parity = steps % 2 == 0
        start = (65, 65)
        seen = set()
        cur = deque()
        cur.append(start)
        seen.add(start)

        odd_count = 1 if parity else 0
        even_count = 0 if parity else 1
        counts = []
        remainder = steps % self.height

        for step in range(1, steps):
            next = deque()
            for loc in cur:
                for dr, dc in NEIGHBORS:
                    next_loc = (loc[0] + dr, loc[1] + dc)
                    row = next_loc[0] % self.height
                    col = next_loc[1] % self.height

                    if self.grid[row][col] == '#':
                        continue

                    if next_loc not in seen:
                        seen.add(next_loc)
                        if (step % 2 == 0) == parity:
                            odd_count += 1
                        else:
                            even_count += 1

                        next.append(next_loc)

            if step % self.height == remainder:
                if step % 2 == 1:
                    counts.append(odd_count)
                else:
                    counts.append(even_count)

                if len(counts) == 3:
                    break

            cur = next

        a = counts[0]
        b = counts[1] - counts[0]
        c = counts[2] - counts[1]

        n = steps // self.height

        return ((n * (n - 1)) // 2) * (c - b) + (b * n) + a

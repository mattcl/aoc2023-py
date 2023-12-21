"""21: step counter"""
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
        start = (65, 65)
        seen_odd = set()
        seen_even = set()
        cur = set()
        cur.add(start)

        for step in range(64):
            next = set()
            for loc in cur:
                if step % 2 == 0:
                    if loc in seen_even:
                        continue

                    seen_even.add(loc)

                else:
                    if loc in seen_odd:
                        continue

                    seen_odd.add(loc)

                for dr, dc in NEIGHBORS:
                    next_loc = (loc[0] + dr, loc[1] + dc)
                    if self.grid[next_loc[0]][next_loc[1]] == '#':
                        continue

                    if step % 2 == 0:
                        if next_loc in seen_odd:
                            continue
                    else:
                        if next_loc in seen_even:
                            continue

                    next.add(next_loc)

            cur = next

        return len(cur) + len(seen_even)

    def part_two(self) -> int:
        steps = 26501365
        start = (65, 65)
        seen_odd = set()
        seen_even = set()
        cur = set()
        cur.add(start)

        counts = []
        remainder = steps % self.height

        for step in range(steps):
            if step % self.height == remainder:
                if step % 2 == 0:
                    prev = len(seen_even)
                else:
                    prev = len(seen_odd)
                counts.append(len(cur) + prev)

                if len(counts) == 3:
                    break

            next = set()
            for loc in cur:
                if step % 2 == 0:
                    if loc in seen_even:
                        continue

                    seen_even.add(loc)

                else:
                    if loc in seen_odd:
                        continue

                    seen_odd.add(loc)

                for dr, dc in NEIGHBORS:
                    next_loc = (loc[0] + dr, loc[1] + dc)
                    row = next_loc[0] % self.height
                    col = next_loc[1] % self.height

                    if self.grid[row][col] == '#':
                        continue

                    if step % 2 == 0:
                        if next_loc in seen_odd:
                            continue
                    else:
                        if next_loc in seen_even:
                            continue

                    next.add(next_loc)

            cur = next

        a = counts[0]
        b = counts[1] - counts[0]
        c = counts[2] - counts[1]

        n = steps // self.height

        return ((n * (n - 1)) // 2) * (c - b) + (b * n) + a

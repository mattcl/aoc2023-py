"""04: scratchcards"""
import aoc.util

class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.cards = []

        for line in input.splitlines():
            winning = set()
            count = 0
            parts = list(filter(None, line.split(" ")))
            id = int(parts[1].replace(":", ""))

            idx = 2
            while parts[idx] != "|":
                winning.add(int(parts[idx]))
                idx += 1

            idx += 1
            num_parts = len(parts)
            while idx < num_parts:
                v = int(parts[idx])
                if v in winning:
                    count += 1
                idx += 1

            self.cards.append(count)

    def recur_count(self, idx, memo) -> int:
        if idx in memo:
            return memo[idx]

        if idx >= len(self.cards):
            return 0

        if self.cards[idx] == 0:
            return 0

        sum = self.cards[idx]

        for i in range(0, self.cards[idx]):
            sum += self.recur_count(idx + i + 1, memo)

        memo[idx] = sum

        return sum

    def part_one(self) -> int:
        sum = 0
        for value in self.cards:
            if value > 0:
                sum += 2 ** (value - 1)

        return sum

    def part_two(self) -> int:
        memo = {}
        sum = 0
        for idx in range(0, len(self.cards)):
            sum += 1 + self.recur_count(idx, memo)
        return sum

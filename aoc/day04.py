"""04: scratchcards"""
import aoc.util


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.cards = []
        self.worth_sum = 0

        lines = input.splitlines()
        num_cards = len(lines)
        copies = [1] * num_cards

        for (l_idx, line) in enumerate(lines):
            winning = set()
            count = 0
            parts = line.split()
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

            if count > 0:
                self.worth_sum += 2 ** (count - 1)

            for j in range(l_idx + 1, l_idx + count + 1):
                copies[j] += copies[l_idx]

        self.num_copies = sum(copies)

    def part_one(self) -> int:
        return self.worth_sum

    def part_two(self) -> int:
        return self.num_copies

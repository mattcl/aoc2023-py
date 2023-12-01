"""01: Trebuchet"""
import aoc.util


STARTING = set(['o', 't', 'f', 's', 'e', 'n'])


# all solutions should subclass the `Solver` exposed by `aoc.util`
# this class MUST be called Solver for the CLI discovery to work
class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)
        lines = input.splitlines()

        self.p1_sum = 0
        self.p2_sum = 0

        for line in lines:
            line_len = len(line)

            start = 0
            end = 0

            for s_idx in range(0, line_len):
                v = self.match_line(s_idx, line)
                if v is not None:
                    self.p2_sum += v * 10
                    start = s_idx
                    break

            for s_idx in range(0, line_len):
                v = self.match_line(line_len - 1 - s_idx, line)
                if v is not None:
                    self.p2_sum += v
                    end = s_idx
                    break

            for s_idx in range(start, line_len):
                if line[s_idx].isdigit():
                    self.p1_sum += int(line[s_idx]) * 10
                    break

            for s_idx in range(end, line_len):
                adjust = line_len - 1 - s_idx
                if line[adjust].isdigit():
                    self.p1_sum += int(line[adjust])
                    break

    def match_simple_digit(self, ch: str):
        if ch.isdigit():
            return int(ch)
        else:
            return None

    def match_line(self, idx: int, line: str):
        first = line[idx]
        if first.isdigit():
            return int(first)
        elif first in STARTING:
            if first == "t":
                if line.startswith("two", idx):
                    return 2
                elif line.startswith("three", idx):
                    return 3
            elif first == "s":
                if line.startswith("six", idx):
                    return 6
                elif line.startswith("seven", idx):
                    return 7
            elif first == "f":
                if line.startswith("four", idx):
                    return 4
                elif line.startswith("five", idx):
                    return 5
            elif line.startswith("one", idx):
                return 1
            elif line.startswith("eight", idx):
                return 8
            elif line.startswith("nine", idx):
                return 9

        return None

    def part_one(self) -> int:
        return self.p1_sum

    def part_two(self) -> int:
        return self.p2_sum

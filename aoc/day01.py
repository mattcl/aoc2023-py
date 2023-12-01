"""01: Trebuchet"""
import aoc.util


# all solutions should subclass the `Solver` exposed by `aoc.util`
# this class MUST be called Solver for the CLI discovery to work
class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)
        self.lines = input.splitlines()

    def match_simple_digit(self, ch: str):
        if ch.isdigit():
            return int(ch)
        else:
            return None

    def match_line(self, idx: int, line: str):
        first = line[idx]
        if first.isdigit():
            return int(first)
        elif first == "t":
            if line.startswith("two", idx):
                return 2
            elif line.startswith("three", idx):
                return 3
            else:
                return None
        elif first == "s":
            if line.startswith("six", idx):
                return 6
            elif line.startswith("seven", idx):
                return 7
            else:
                return None
        elif first == "f":
            if line.startswith("four", idx):
                return 4
            elif line.startswith("five", idx):
                return 5
            else:
                return None
        elif line.startswith("one", idx):
            return 1
        elif line.startswith("eight", idx):
            return 8
        elif line.startswith("nine", idx):
            return 9
        else:
            return None

    def part_one(self) -> int:
        sum = 0
        for line in self.lines:
            for ch in line:
                v = self.match_simple_digit(ch)
                if v is not None:
                    sum += v * 10
                    break

            l = len(line)

            for i in range(0, l):
                ch = line[l - 1 - i]
                v = self.match_simple_digit(ch)
                if v is not None:
                    sum += v
                    break

        return sum

    def part_two(self) -> int:
        sum = 0
        for line in self.lines:
            line_len = len(line)

            for s_idx in range(0, line_len):
                v = self.match_line(s_idx, line)
                if v is not None:
                    sum += v * 10
                    break

            for s_idx in range(0, line_len):
                v = self.match_line(line_len - 1 - s_idx, line)
                if v is not None:
                    sum += v
                    break

        return sum

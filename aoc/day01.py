"""01: Trebuchet"""
import aoc.util


# all solutions should subclass the `Solver` exposed by `aoc.util`
# this class MUST be called Solver for the CLI discovery to work
class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)
        self.lines = self.input.splitlines()

    def match_simple_digit(self, ch: str):
        if ch.isdigit():
            return int(ch)
        else:
            return None

    def match_slice(self, slice: str):
        if slice[0].isdigit():
            return int(slice[0])
        if slice.startswith("zero"):
            return 0
        elif slice.startswith("one"):
            return 1
        elif slice.startswith("two"):
            return 2
        elif slice.startswith("three"):
            return 3
        elif slice.startswith("four"):
            return 4
        elif slice.startswith("five"):
            return 5
        elif slice.startswith("six"):
            return 6
        elif slice.startswith("seven"):
            return 7
        elif slice.startswith("eight"):
            return 8
        elif slice.startswith("nine"):
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
                slice = line[s_idx:]
                v = self.match_slice(slice)
                if v is not None:
                    sum += v * 10
                    break

            for s_idx in range(0, line_len):
                slice = line[(line_len - 1 - s_idx):]
                v = self.match_slice(slice)
                if v is not None:
                    sum += v
                    break

        return sum

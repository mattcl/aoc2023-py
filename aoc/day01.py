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
        if ch == '0':
            return 0
        elif ch == '1':
            return 1
        elif ch == '2':
            return 2
        elif ch == '3':
            return 3
        elif ch == '4':
            return 4
        elif ch == '5':
            return 5
        elif ch == '6':
            return 6
        elif ch == '7':
            return 7
        elif ch == '8':
            return 8
        elif ch == '9':
            return 9
        else:
            return None

    def match_slice(self, slice: str):
        if slice.startswith("0") or slice.startswith("zero"):
            return 0
        elif slice.startswith("1") or slice.startswith("one"):
            return 1
        elif slice.startswith("2") or slice.startswith("two"):
            return 2
        elif slice.startswith("3") or slice.startswith("three"):
            return 3
        elif slice.startswith("4") or slice.startswith("four"):
            return 4
        elif slice.startswith("5") or slice.startswith("five"):
            return 5
        elif slice.startswith("6") or slice.startswith("six"):
            return 6
        elif slice.startswith("7") or slice.startswith("seven"):
            return 7
        elif slice.startswith("8") or slice.startswith("eight"):
            return 8
        elif slice.startswith("9") or slice.startswith("nine"):
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

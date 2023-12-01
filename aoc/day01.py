"""01: Trebuchet"""
import aoc.util


def one(idx: int, line: str):
    if line.startswith("ne", idx):
        return 1
    else:
        return None


def two_three(idx: int, line: str):
    if line.startswith("wo", idx):
        return 2
    elif line.startswith("hree", idx):
        return 3
    else:
        return None


def four_five(idx: int, line: str):
    if line.startswith("our", idx):
        return 4
    elif line.startswith("ive", idx):
        return 5
    else:
        return None


def six_seven(idx: int, line: str):
    if line.startswith("ix", idx):
        return 6
    elif line.startswith("even", idx):
        return 7
    else:
        return None


def eight(idx: int, line: str):
    if line.startswith("ight", idx):
        return 8
    else:
        return None


def nine(idx: int, line: str):
    if line.startswith("ine", idx):
        return 9
    else:
        return None


STARTING = {
    'o': one,
    't': two_three,
    'f': four_five,
    's': six_seven,
    'e': eight,
    'n': nine,
    # this is slightly faster than checking isdigit() then parsing to int()
    '0': lambda _a, _b: 0,
    '1': lambda _a, _b: 1,
    '2': lambda _a, _b: 2,
    '3': lambda _a, _b: 3,
    '4': lambda _a, _b: 4,
    '5': lambda _a, _b: 5,
    '6': lambda _a, _b: 6,
    '7': lambda _a, _b: 7,
    '8': lambda _a, _b: 8,
    '9': lambda _a, _b: 9,
}

# this is slightly faster than checking isdigit() then parsing to int()
DIGIT_MAP = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
}


def match_line(idx: int, line: str):
    first = line[idx]
    if first in STARTING:
        return STARTING[first](idx + 1, line)
    else:
        return None


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
                v = match_line(s_idx, line)
                if v is not None:
                    self.p2_sum += v * 10
                    start = s_idx
                    break

            for s_idx in range(line_len - 1, -1, -1):
                v = match_line(s_idx, line)
                if v is not None:
                    self.p2_sum += v
                    end = s_idx
                    break

            for s_idx in range(start, line_len):
                v = DIGIT_MAP.get(line[s_idx])
                if v is not None:
                    self.p1_sum += v * 10
                    break

            for s_idx in range(end, -1, -1):
                v = DIGIT_MAP.get(line[s_idx])
                if v is not None:
                    self.p1_sum += v
                    break

    def part_one(self) -> int:
        return self.p1_sum

    def part_two(self) -> int:
        return self.p2_sum

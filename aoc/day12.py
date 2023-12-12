"""12: hot springs"""
from itertools import islice
from multiprocessing import Pool
import aoc.util


def arrangements(input, groups, seen):
    if len(input) == 0:
        if len(groups) == 0:
            return 1
        return 0

    key = (len(input), len(groups))

    cached = seen.get(key)
    if cached is not None:
        return cached

    first, *remainder = input

    remainder_len = len(remainder)

    match first:
        case '?':
            match groups:
                case []:
                    if all(ch != '#' for ch in remainder):
                        seen[key] = 1
                        return 1
                    else:
                        seen[key] = 0
                        return 0

                case [v, *remaining_groups]:
                    needed = v - 1
                    if needed > remainder_len:
                        seen[key] = 0
                        return 0
                    elif all(ch != '.' for ch in islice(remainder, 0, needed)):
                        if remainder_len == needed:
                            if len(remaining_groups) == 0:
                                seen[key] = 1
                                return 1
                            else:
                                seen[key] = 0
                                return 0

                        if remainder[needed] != '#':
                            res = arrangements(remainder[needed + 1:], remaining_groups, seen)
                            res += arrangements(remainder, groups, seen)
                            seen[key] = res
                            return res

                    res = arrangements(remainder, groups, seen)
                    seen[key] = res
                    return res

        case '#':
            match groups:
                case []:
                    seen[key] = 0
                    return 0

                case [v, *remaining_groups]:
                    needed = v - 1
                    if needed > remainder_len:
                        seen[key] = 0
                        return 0
                    elif all(ch != '.' for ch in islice(remainder, 0, needed)):
                        if remainder_len == needed:
                            if len(remaining_groups) == 0:
                                seen[key] = 1
                                return 1
                            else:
                                seen[key] = 0
                                return 0

                        if remainder[needed] != '#':
                            res = arrangements(remainder[needed + 1:], remaining_groups, seen)
                            seen[key] = res
                            return res

                    seen[key] = 0
                    return 0

        case '.':
            res = arrangements(remainder, groups, seen)
            seen[key] = res
            return res

    assert False, "we should not get here"


def process(spring):
    seen = {}
    return arrangements(spring[0], spring[1], seen)


def process_long(spring):
    seen = {}
    return arrangements(spring[2], spring[3], seen)


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.springs = []
        for line in input.splitlines():
            parts = line.split()
            text = parts[0]
            nums = list(map(int, parts[1].split(",")))
            long_text = "?".join([text] * 5)
            long_nums = nums * 5
            self.springs.append([text, nums, long_text, long_nums])

        # do this here so we can make sure we terminate the pool
        with Pool() as pool:
            self.p1 = sum(pool.map(process, self.springs))
            self.p2 = sum(pool.map(process_long, self.springs))

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2

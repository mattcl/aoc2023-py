"""12: hot springs"""
from itertools import islice
from multiprocessing import Pool
import aoc.util


def arrangements(input, groups, seen):
    input_len = len(input)
    group_len = len(groups)
    if group_len == 0:
        if input_len > 0 and '#' in input:
            return 0
        return 1

    if input_len == 0:
        return 0

    key = (input_len, group_len)

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
            for i in range(0, input_len - 1):
                if remainder[i] in "#?":
                    res = arrangements(remainder[i:], groups, seen)
                    seen[key] = res
                    return res

            if group_len == 0:
                return 1
            return 0

    assert False, "we should not get here"


def process(spring):
    seen = {}
    return arrangements(spring[0], spring[1], seen)


def process_long(spring):
    txt = "?".join([spring[0]] * 5)
    long_nums = spring[1] * 5
    seen = {}
    return arrangements(txt, long_nums, seen)


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        springs = []
        for line in input.splitlines():
            parts = line.split()
            text = parts[0]
            nums = list(map(int, parts[1].split(",")))
            springs.append([text, nums])

        # do this here so we can make sure we terminate the pool
        with Pool() as pool:
            self.p1 = sum(pool.map(process, springs))
            self.p2 = sum(pool.map(process_long, springs))

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2

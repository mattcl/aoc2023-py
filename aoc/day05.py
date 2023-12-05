"""05: If You Give A Seed A Fertilizer"""
import aoc.util


class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, v):
        return v >= self.start and v <= self.end


class Entry:
    def __init__(self, dest, source, length):
        self.dest = Range(dest, dest + length - 1)
        self.source = Range(source, source + length - 1)

    def translate(self, v):
        if self.source.contains(v):
            return self.dest.start + v - self.source.start
        else:
            return None

    def contains(self, other):
        return self.source.start <= other.start and other.end <= self.source.end

    def right_of_overlapping(self, other):
        return other.start < self.source.start and self.source.start <= other.end and other.end <= self.source.end

    def left_of_overlapping(self, other):
        return self.source.start <= other.start and other.start <= self.source.end and self.source.end < other.end

    def is_contained_by(self, other):
        return other.start < self.source.start and self.source.end < other.end


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        groups = input.split("\n\n")
        self.seeds = list(map(int, groups[0].strip().replace("seeds: ", "").split()))
        self.range_maps = []

        for i in range(1, len(groups)):
            lines = groups[i].splitlines()
            entries = []
            for j in range(1, len(lines)):
                vals = list(map(int, lines[j].strip().split()))
                entries.append(Entry(vals[0], vals[1], vals[2]))

            entries.sort(key=lambda x: x.source.start)
            self.range_maps.append(entries)

    def part_one(self) -> int:
        lowest = None
        for seed in self.seeds:
            v = seed
            for mapping in self.range_maps:
                for entry in mapping:
                    t = entry.translate(v)
                    if t is not None:
                        v = t
                        break

            if lowest is None or v < lowest:
                lowest = v

        return lowest

    def part_two(self) -> int:
        ranges = []
        for i in range(0, len(self.seeds), 2):
            ranges.append(Range(self.seeds[i], self.seeds[i] + self.seeds[i + 1] - 1))

        for mapping in self.range_maps:
            next_ranges = []

            while len(ranges) > 0:
                r = ranges.pop()
                found = False
                for entry in mapping:
                    if entry.contains(r):
                        next_ranges.append(
                            Range(
                                r.start + entry.dest.start - entry.source.start,
                                r.end + entry.dest.start - entry.source.start
                            )
                        )
                        found = True
                        break
                    elif entry.right_of_overlapping(r):
                        next_ranges.append(
                            Range(
                                r.start,
                                entry.source.start - 1
                            )
                        )
                        next_ranges.append(
                            Range(
                                entry.dest.start,
                                r.end + entry.dest.start - entry.source.start
                            )
                        )
                        found = True
                        break
                    elif entry.left_of_overlapping(r):
                        next_ranges.append(
                            Range(
                                r.start + entry.dest.start - entry.source.start,
                                entry.source.end + entry.dest.start - r.start
                            )
                        )
                        ranges.append(
                            Range(
                                entry.source.end + 1,
                                r.end,
                            )
                        )
                        found = True
                        break
                    elif entry.is_contained_by(r):
                        next_ranges.append(
                            Range(
                                r.start,
                                entry.source.start - 1
                            )
                        )
                        next_ranges.append(
                            Range(
                                entry.dest.start,
                                entry.dest.end
                            )
                        )
                        ranges.append(
                            Range(
                                entry.source.end + 1,
                                r.end
                            )
                        )
                        found = True
                        break

                if found:
                    continue

                # put ourself back if we didn't overlap anything
                next_ranges.append(r)

            ranges = next_ranges

        lowest = None

        for r in ranges:
            if lowest is None or r.start < lowest:
                lowest = r.start

        return lowest

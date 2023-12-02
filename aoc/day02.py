"""02: cube conundrum"""
import aoc.util


class CubeSet:
    @classmethod
    def from_str(cls, input: str):
        parts = input.split(", ")
        r = 0
        g = 0
        b = 0
        for part in parts:
            sub_parts = part.split(" ")
            v = int(sub_parts[0])
            if sub_parts[1][0] == 'r':
                r = max(v, r)
            elif sub_parts[1][0] == 'g':
                g = max(v, g)
            elif sub_parts[1][0] == 'b':
                b = max(v, b)

        return cls(r, g, b)

    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def maximum(self, other):
        self.r = max(self.r, other.r)
        self.g = max(self.g, other.g)
        self.b = max(self.b, other.b)

    def subset(self, other) -> bool:
        return self.r <= other.r and self.g <= other.g and self.b <= other.b

    def power(self) -> int:
        return self.r * self.g * self.b


COMPARE = CubeSet(12, 13, 14)


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)
        self.id_sum = 0
        self.min_prod = 0

        for line in input.splitlines():
            # get the id
            parts = line.split(": ")
            id = int(parts[0].split(" ")[1])

            # we can just parse all the sets as if they were one beause of the
            # way we parse
            minimum = CubeSet.from_str(parts[1].replace(";", ","))

            if minimum.subset(COMPARE):
                self.id_sum += id

            self.min_prod += minimum.power()

    def part_one(self) -> int:
        # again, more efficient in this case to do both at the same time
        return self.id_sum

    def part_two(self) -> int:
        return self.min_prod

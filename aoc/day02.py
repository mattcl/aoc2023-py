# You can copy/paste this template to start a new day

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


class Game:
    def __init__(self, id: int, s: CubeSet):
        self.id = id
        self.minimum = s


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)
        self.games = []
        for line in input.splitlines():
            # get the id
            parts = line.split(": ")
            id = int(parts[0].split(" ")[1])

            minimum = CubeSet(0, 0, 0)
            for part in parts[1].split("; "):
                minimum.maximum(CubeSet.from_str(part))

            self.games.append(Game(id, minimum))

    def part_one(self) -> int:
        s = CubeSet(12, 13, 14)
        sum = 0
        for g in self.games:
            if g.minimum.subset(s):
                sum += g.id

        return sum

    def part_two(self) -> int:
        sum = 0
        for g in self.games:
            sum += g.minimum.power()

        return sum

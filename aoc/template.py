# You can copy/paste this template to start a new day

"""DAY: PROBLEM NAME"""
import aoc.util


# all solutions should subclass the `Solver` exposed by `aoc.util`
# this class MUST be called Solver for the CLI discovery to work
class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)

        # optionally do something with self.input, like parsing it to a more
        # useful representation and storing it in the instance

    def part_one(self) -> int:
        # TODO: actually return the answer
        return 0

    def part_two(self) -> int:
        # TODO: actually return the answer
        return 0

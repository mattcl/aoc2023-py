class Solution(object):
    """This is a wrapper to handle solutions to problems in a consistent way.

    This ensures that we render the solutions consistently.
    """

    def __init__(self, part_one, part_two):
        self.part_one = part_one
        self.part_two = part_two

    def __eq__(self, other):
        return self.part_one == other.part_one and self.part_two == other.part_two

    def to_string(self, json: bool) -> str:
        if json:
            # avoid the overhead of loading the json module unless we have to
            import json

            # we can get away with this because there shouldn't be any
            # additional attrs added to this class
            return json.dumps(self.__dict__)
        else:
            return f"part one: {self.part_one}\npart two: {self.part_two}"


class Solver(object):
    """This provides a consistent interface that the CLI can leverage to
    evaluate solutions.

    The CLI will provide the content of the input files as a string, thus
    abstracting away the file handling.
    """

    @classmethod
    def solve(cls, input: str) -> Solution:
        inst = cls(input)
        return Solution(inst.part_one(), inst.part_two())

    def __init__(self, input: str):
        # by default we just store the input that was given to us
        self.input = input

    def part_one(self):
        return "not implemented"

    def part_two(self):
        return "not implemented"

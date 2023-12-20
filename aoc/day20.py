"""20: PROBLEM NAME"""
from collections import deque
from copy import deepcopy
from itertools import product
import aoc.util


class Module:
    def __init__(self, input: str):
        parts = input.split(" -> ")
        if parts[0] == "broadcaster":
            self.kind = "b"
            self.name = "broadcaster"
        else:
            self.kind = parts[0][0]
            self.name = parts[0][1:]
        self.destinations = parts[1].split(", ")

        if self.kind == '&':
            self.inputs = {}
        elif self.kind == '%':
            self.state = False


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        self.modules = {}
        self.cycle_conjunction_key = None
        for line in input.splitlines():
            module = Module(line)
            if "rx" in module.destinations:
                self.cycle_conjunction_key = module.name
            self.modules[module.name] = module

        # set all the input tracking for the conjunctions
        for k, v in self.modules.items():
            for d in v.destinations:
                if d in self.modules and self.modules[d].kind == '&':
                    self.modules[d].inputs[k] = False

    def part_one(self) -> int:
        modules = deepcopy(self.modules)
        pulses = deque()
        low_pulses = 0
        high_pulses = 0
        for _ in range(0, 1000):
            pulses.append(("button", "broadcaster", False))
            low_pulses += 1

            while len(pulses) > 0:
                origin, dest, pulse = pulses.popleft()

                if dest in modules:
                    match modules[dest].kind:
                        case '%':
                            if pulse:
                                continue

                            destinations = modules[dest].destinations
                            modules[dest].state = not modules[dest].state
                            if modules[dest].state:
                                high_pulses += len(destinations)
                                next_pulse = True
                            else:
                                low_pulses += len(destinations)
                                next_pulse = False

                            pulses.extend((dest, d, next_pulse) for d in destinations)
                        case '&':
                            destinations = modules[dest].destinations
                            modules[dest].inputs[origin] = pulse
                            if all(modules[dest].inputs.values()):
                                low_pulses += len(destinations)
                                next_pulse = False
                            else:
                                high_pulses += len(destinations)
                                next_pulse = True

                            pulses.extend((dest, d, next_pulse) for d in destinations)
                        case 'b':
                            destinations = modules[dest].destinations
                            if pulse:
                                high_pulses += len(destinations)
                            else:
                                low_pulses += len(destinations)

                            pulses.extend((dest, d, pulse) for d in destinations)

        return low_pulses * high_pulses

    def part_two(self) -> int:
        pulses = deque()
        cycle_detect = {}

        for i in self.modules[self.cycle_conjunction_key].inputs.keys():
            cycle_detect[i] = []

        count = 0
        while True:
            pulses.append(("button", "broadcaster", False))

            while len(pulses) > 0:
                origin, dest, pulse = pulses.popleft()

                if dest in self.modules:
                    match self.modules[dest].kind:
                        case '%':
                            if pulse:
                                continue

                            destinations = self.modules[dest].destinations
                            self.modules[dest].state = not self.modules[dest].state
                            if self.modules[dest].state:
                                next_pulse = True
                            else:
                                next_pulse = False

                            pulses.extend((dest, d, next_pulse) for d in destinations)
                        case '&':
                            if dest == self.cycle_conjunction_key:
                                if pulse:
                                    cycle_detect[origin].append(count + 1)

                                    # we're making the same dumb assumption as
                                    # in my rust solution. If it doesn't hold,
                                    # we'll have to actually determine the cycle
                                    # length and LCM the intervals
                                    if all(len(x) > 0 for x in cycle_detect.values()):
                                        prod = 1
                                        for v in cycle_detect.values():
                                            prod *= v[0]

                                        return prod

                            destinations = self.modules[dest].destinations
                            self.modules[dest].inputs[origin] = pulse
                            if all(self.modules[dest].inputs.values()):
                                next_pulse = False
                            else:
                                next_pulse = True

                            pulses.extend((dest, d, next_pulse) for d in destinations)
                        case 'b':
                            destinations = self.modules[dest].destinations
                            pulses.extend((dest, d, pulse) for d in destinations)

            count += 1

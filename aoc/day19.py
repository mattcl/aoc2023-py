"""19: aplenty"""
from collections import deque
import aoc.util


GT = 0
LT = 1
WF = 2


class Rule:
    def __init__(self, input):
        if '<' in input:
            parts = input.split(':')
            self.kind = LT
            self.key = parts[0][0]
            self.value = int(parts[0][2:])
            self.workflow = parts[1]
        elif '>' in input:
            parts = input.split(':')
            self.kind = GT
            self.key = parts[0][0]
            self.value = int(parts[0][2:])
            self.workflow = parts[1]
        else:
            self.kind = WF
            self.workflow = input

    def process(self, part):
        match self.kind:
            case 0:
                if part[self.key] > self.value:
                    return self.workflow
            case 1:
                if part[self.key] < self.value:
                    return self.workflow
            case 2:
                return self.workflow

        return None


class Solver(aoc.util.Solver):
    def part_one(self) -> int:
        total = 0
        for part in self.parts:
            workflow = "in"
            done = False
            while not done:
                cur_rules = self.workflows[workflow]
                for rule in cur_rules:
                    wf = rule.process(part)
                    if wf is None:
                        continue

                    if wf == 'A':
                        total += part['x'] + part['m'] + part['a'] + part['s']
                        done = True
                        break

                    if wf == 'R':
                        done = True
                        break

                    workflow = wf
                    break

        return total

    def part_two(self) -> int:
        intervals = deque()
        intervals.append(((1, 4000), (1, 4000), (1, 4000), (1, 4000), "in", 0))
        total = 0

        while len(intervals) > 0:
            x, m, a, s, wf, rule_idx = intervals.pop()

            if wf == 'A':
                total += (x[1] - x[0] + 1) * (m[1] - m[0] + 1) * (a[1] - a[0] + 1) * (s[1] - s[0] + 1)
            elif wf != 'R':
                cur_rules = self.workflows[wf]
                cur_rule = cur_rules[rule_idx]

                match cur_rule.kind:
                    # greater
                    case 0:
                        match cur_rule.key:
                            case 'x':
                                adjusted = cur_rule.value + 1
                                if adjusted >= x[0] and adjusted <= x[1]:
                                    intervals.append(((adjusted, x[1]), m, a, s, cur_rule.workflow, 0))

                                if cur_rule.value >= x[0] and cur_rule.value <= x[1]:
                                    intervals.append(((x[0], cur_rule.value), m, a, s, wf, rule_idx + 1))
                            case 'm':
                                adjusted = cur_rule.value + 1
                                if adjusted >= m[0] and adjusted <= m[1]:
                                    intervals.append((x, (adjusted, m[1]), a, s, cur_rule.workflow, 0))

                                if cur_rule.value >= m[0] and cur_rule.value <= m[1]:
                                    intervals.append((x, (m[0], cur_rule.value), a, s, wf, rule_idx + 1))
                            case 'a':
                                adjusted = cur_rule.value + 1
                                if adjusted >= a[0] and adjusted <= a[1]:
                                    intervals.append((x, m, (adjusted, a[1]), s, cur_rule.workflow, 0))

                                if cur_rule.value >= a[0] and cur_rule.value <= a[1]:
                                    intervals.append((x, m, (a[0], cur_rule.value), s, wf, rule_idx + 1))
                            case 's':
                                adjusted = cur_rule.value + 1
                                if adjusted >= s[0] and adjusted <= s[1]:
                                    intervals.append((x, m, a, (adjusted, s[1]), cur_rule.workflow, 0))

                                if cur_rule.value >= s[0] and cur_rule.value <= s[1]:
                                    intervals.append((x, m, a, (s[0], cur_rule.value), wf, rule_idx + 1))
                    # less
                    case 1:
                        match cur_rule.key:
                            case 'x':
                                adjusted = cur_rule.value - 1
                                if adjusted >= x[0] and adjusted <= x[1]:
                                    intervals.append(((x[0], adjusted), m, a, s, cur_rule.workflow, 0))

                                if cur_rule.value >= x[0] and cur_rule.value <= x[1]:
                                    intervals.append(((cur_rule.value, x[1]), m, a, s, wf, rule_idx + 1))
                            case 'm':
                                adjusted = cur_rule.value - 1
                                if adjusted >= m[0] and adjusted <= m[1]:
                                    intervals.append((x, (m[0], adjusted), a, s, cur_rule.workflow, 0))

                                if cur_rule.value >= m[0] and cur_rule.value <= m[1]:
                                    intervals.append((x, (cur_rule.value, m[1]), a, s, wf, rule_idx + 1))
                            case 'a':
                                adjusted = cur_rule.value - 1
                                if adjusted >= a[0] and adjusted <= a[1]:
                                    intervals.append((x, m, (a[0], adjusted), s, cur_rule.workflow, 0))

                                if cur_rule.value >= a[0] and cur_rule.value <= a[1]:
                                    intervals.append((x, m, (cur_rule.value, a[1]), s, wf, rule_idx + 1))
                            case 's':
                                adjusted = cur_rule.value - 1
                                if adjusted >= s[0] and adjusted <= s[1]:
                                    intervals.append((x, m, a, (s[0], adjusted), cur_rule.workflow, 0))

                                if cur_rule.value >= s[0] and cur_rule.value <= s[1]:
                                    intervals.append((x, m, a, (cur_rule.value, s[1]), wf, rule_idx + 1))
                    case 2:
                        intervals.append((x, m, a, s, cur_rule.workflow, 0))

        return total

    def __init__(self, input: str):
        self.workflows = {}
        self.parts = []
        workflows, parts = input.split("\n\n")

        for line in workflows.splitlines():
            key, remainder = line.split("{")
            self.workflows[key] = list(map(Rule, remainder[:-1].split(',')))

        for line in parts.splitlines():
            part = {}
            for p in line[1:-1].split(','):
                part[p[0]] = int(p[2:])

            self.parts.append(part)


"""07: PROBLEM NAME"""
from operator import attrgetter
import aoc.util

JOKER = 'k'

CARD_MAP = {
    '2': 'b',
    '3': 'c',
    '4': 'd',
    '5': 'e',
    '6': 'f',
    '7': 'g',
    '8': 'h',
    '9': 'i',
    'T': 'j',
    'J': JOKER,
    'Q': 'l',
    'K': 'm',
    'A': 'n',
}


def hand_kinds(cards):
    counts = {}
    max_count = 0
    max_jokerless = 0
    for c in cards:
        v = counts.get(c, 0) + 1
        if v > max_count:
            max_count = v
        if c != JOKER and v > max_jokerless:
            max_jokerless = v
        counts[c] = v

    if max_count == 5:
        # our highest value
        return 3, 3

    different = len(counts)

    normal_score = max_count - different

    joker_count = counts.get(JOKER, 0)

    if joker_count == 0:
        return normal_score, normal_score

    if different < 3:
        joker_score = 3
    else:
        joker_score = max_jokerless + joker_count - different + 1

    return normal_score, joker_score


class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.kind, self.joker_kind = hand_kinds(self.cards)
        self.joker_cards = self.cards.replace(JOKER, 'a')
        self.bid = bid


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)
        self.hands = []
        for line in input.splitlines():
            parts = line.split()
            cards = "".join(map(lambda x: CARD_MAP[x], parts[0]))
            bid = int(parts[1])
            self.hands.append(Hand(cards, bid))

    def part_one(self) -> int:
        self.hands.sort(key=attrgetter('kind', 'cards'))
        return sum((idx + 1) * v.bid for (idx, v) in enumerate(self.hands))

    def part_two(self) -> int:
        self.hands.sort(key=attrgetter('joker_kind', 'joker_cards'))
        return sum((idx + 1) * v.bid for (idx, v) in enumerate(self.hands))

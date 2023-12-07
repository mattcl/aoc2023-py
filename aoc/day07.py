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


HIGH_CARD = 0
ONE_PAIR = 1
TWO_PAIR = 2
THREE_KIND = 3
FULL_HOUSE = 4
FOUR_KIND = 5
FIVE_KIND = 6


def hand_kinds(cards):
    counts = {}
    maximum = 0
    for c in cards:
        if c not in counts:
            counts[c] = 0
        counts[c] += 1
        if counts[c] > maximum:
            maximum = counts[c]

    joker_count = counts.get(JOKER, 0)
    num = len(counts)

    if num == 1:
        return FIVE_KIND, FIVE_KIND

    if num == 5:
        if joker_count > 0:
            return HIGH_CARD, ONE_PAIR
        else:
            return HIGH_CARD, HIGH_CARD

    if num == 2:
        if maximum == 4:
            if joker_count > 0:
                return FOUR_KIND, FIVE_KIND
            else:
                return FOUR_KIND, FOUR_KIND
        else:
            if joker_count > 0:
                return FULL_HOUSE, FIVE_KIND
            else:
                return FULL_HOUSE, FULL_HOUSE

    if maximum == 3:
        if joker_count > 0:
            return THREE_KIND, FOUR_KIND
        else:
            return THREE_KIND, THREE_KIND

    if num == 4:
        if joker_count > 0:
            return ONE_PAIR, THREE_KIND
        else:
            return ONE_PAIR, ONE_PAIR

    match joker_count:
        case 1:
            return TWO_PAIR, FULL_HOUSE
        case 2:
            return TWO_PAIR, FOUR_KIND
        case _:
            return TWO_PAIR, TWO_PAIR


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

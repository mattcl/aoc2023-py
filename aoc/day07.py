"""07: PROBLEM NAME"""
from operator import attrgetter
import aoc.util

JOKER = 16
JOKER_MASK = ~JOKER

CARD_MAP = {
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'J': JOKER,
    'Q': 32,
    'K': 33,
    'A': 34,
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
    for c in cards:
        if c not in counts:
            counts[c] = 0
        counts[c] += 1

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
        for value in counts.values():
            if value == 4 or value == 1:
                if joker_count > 0:
                    return FOUR_KIND, FIVE_KIND
                else:
                    return FOUR_KIND, FOUR_KIND
            elif value == 2 or value == 3:
                if joker_count > 0:
                    return FULL_HOUSE, FIVE_KIND
                else:
                    return FULL_HOUSE, FULL_HOUSE

    num_pairs = 0
    for value in counts.values():
        if value == 3:
            if joker_count == 1 or joker_count == 3:
                return THREE_KIND, FOUR_KIND
            else:
                return THREE_KIND, THREE_KIND

        if value == 2:
            num_pairs += 1

    if num_pairs == 2:
        match joker_count:
            case 1:
                return TWO_PAIR, FULL_HOUSE
            case 2:
                return TWO_PAIR, FOUR_KIND
            case _:
                return TWO_PAIR, TWO_PAIR

    if joker_count > 0:
        return ONE_PAIR, THREE_KIND
    else:
        return ONE_PAIR, ONE_PAIR


class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.kind, self.joker_kind = hand_kinds(self.cards)
        self.joker_cards = list(map(lambda x: x & JOKER_MASK, self.cards))
        self.bid = bid


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)
        self.hands = []
        for line in input.splitlines():
            parts = line.split()
            cards = list(map(lambda x: CARD_MAP[x], parts[0]))
            bid = int(parts[1])
            self.hands.append(Hand(cards, bid))

    def part_one(self) -> int:
        self.hands.sort(key=attrgetter('kind', 'cards'))
        return sum((idx + 1) * v.bid for (idx, v) in enumerate(self.hands))

    def part_two(self) -> int:
        self.hands.sort(key=attrgetter('joker_kind', 'joker_cards'))
        return sum((idx + 1) * v.bid for (idx, v) in enumerate(self.hands))

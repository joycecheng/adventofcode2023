from collections import defaultdict, namedtuple
from enum import IntEnum
import sys

class HandType(IntEnum):
    HighCard = 0
    OnePair = 1
    TwoPair = 2
    ThreeOfAKind=3
    FullHouse=4
    FourOfAKind=5
    FiveOfAKind=6

def get_hand_type(hand):
    counts = defaultdict(lambda: 0)
    for card in hand:
        counts[card] += 1

    ordered_counts = list(reversed(sorted(counts.values())))

    if ordered_counts[0] == 1:
        t = HandType.HighCard
    elif ordered_counts[0] == 2 and ordered_counts[1] == 1:
        t = HandType.OnePair
    elif ordered_counts[0] == 2 and ordered_counts[1] == 2:
        t = HandType.TwoPair
    elif ordered_counts[0] == 3 and ordered_counts[1] == 1:
        t = HandType.ThreeOfAKind
    elif ordered_counts[0] == 3 and ordered_counts[1] == 2:
        t = HandType.FullHouse
    elif ordered_counts[0] == 4:
        t = HandType.FourOfAKind
    else:
        t = HandType.FiveOfAKind

    return t

def get_hand_type(hand):
    jcount = hand.count(CardFace.J)
    hand = [ card for card in hand if card != CardFace.J ]

    if len(hand) == 0:
        return HandType.FiveOfAKind

    counts = defaultdict(lambda: 0)
    for card in hand:
        counts[card] += 1

    ordered_counts = list(reversed(sorted(counts.values())))
    ordered_counts[0] += jcount

    if ordered_counts[0] == 1:
        t = HandType.HighCard
    elif ordered_counts[0] == 2 and ordered_counts[1] == 1:
        t = HandType.OnePair
    elif ordered_counts[0] == 2 and ordered_counts[1] == 2:
        t = HandType.TwoPair
    elif ordered_counts[0] == 3 and ordered_counts[1] == 1:
        t = HandType.ThreeOfAKind
    elif ordered_counts[0] == 3 and ordered_counts[1] == 2:
        t = HandType.FullHouse
    elif ordered_counts[0] == 4:
        t = HandType.FourOfAKind
    else:
        t = HandType.FiveOfAKind

    return t

class CardFace(IntEnum):
    J = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    T = 10
    Q = 12
    K = 13
    A = 14

card_face_map = {
        "2": CardFace.Two,
        "3": CardFace.Three,
        "4": CardFace.Four,
        "5": CardFace.Five,
        "6": CardFace.Six,
        "7": CardFace.Seven,
        "8": CardFace.Eight,
        "9": CardFace.Nine,
        "T": CardFace.T,
        "J": CardFace.J,
        "Q": CardFace.Q,
        "K": CardFace.K,
        "A": CardFace.A,
}
def parse_card_face(cards):
    return [ card_face_map[card] for card in cards ]

Hand = namedtuple("Hand", ["type", "cards", "bid"])

def parse(lines):
    hands = []
    bids = []
    for line in lines:
        hand, bid = line.split(" ")
        hand = parse_card_face(hand)
        hands.append(Hand(get_hand_type(hand), hand, int(bid)))
        bids.append(bid)

    return hands

hands = parse(open(sys.argv[1]).readlines())

winnings = 0
for i, hand in enumerate(sorted(hands)):
    print(i, hand)
    winnings += (i+1) * int(hand.bid)
print(winnings)

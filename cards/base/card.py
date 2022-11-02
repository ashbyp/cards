import random
import itertools
from cards.base.utils import remove_subsets, sets_to_sorted_lists

SUITS = ('C', 'D', 'H', 'S')

PICTURES = {
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 1,
}

RANK_TO_PICTURES = {v: k for k, v in PICTURES.items()}


class Card:
    def __init__(self, rank, suit):
        try:
            self._rank = int(rank)
            if self._rank < 1 or self._rank > 13:
                raise ValueError('rank must be between 1-13')
        except ValueError as e:
            raise ValueError("rank must be an integer", e)

        if suit not in SUITS:
            raise ValueError(f'suit must be one of {SUITS}')
        self._suit = suit
        self._value = self._rank if self._rank < 11 else 10

    @staticmethod
    def from_str(card_name):
        # AD 1D ad 1d  - all ace diamonds
        # 10S 10s - both 10 spades
        # 5C 5c - both 5 clubs
        # JH Jh 11H 11h - all jack of hearts
        if len(card_name) > 3:
            raise ValueError(f'"{card_name}" invalid format, try one of these formats \'JH Jh 11H 11h\'')
        card_name = card_name.upper()
        rank_str = card_name[0:2] if len(card_name) == 3 else card_name[0]
        if rank_str in PICTURES:
            rank = int(PICTURES[rank_str])
        else:
            rank = int(rank_str)

        suit_name = card_name[-1]
        if suit_name not in SUITS:
            raise ValueError(f'short suit name must be one of {SUITS}')
        return Card(rank, suit_name)

    @staticmethod
    def from_str_list(card_names, sep=','):
        if not card_names:
            return []
        if sep == ',':
            card_names = card_names.replace(' ', '')
        return [Card.from_str(name) for name in card_names.split(sep)]

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    @property
    def value(self):
        return self._value

    def is_next_rank(self, other, ace_high=False):
        return (ace_high and (other.rank == 1 and self.rank == 13)) or (other.rank - self.rank == 1)

    def str_rank(self):
        return RANK_TO_PICTURES.get(self._rank, str(self._rank))

    def _cmp(self, other):
        return (self.rank - other.rank) or (ord(self.suit) - ord(other.suit))

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __le__(self, other):
        return self._cmp(other) <= 0

    def __eq__(self, other):
        return self._cmp(other) == 0

    def __ne__(self, other):
        return self._cmp(other) != 0

    def __ge__(self, other):
        return self._cmp(other) >= 0

    def __gt__(self, other):
        return self._cmp(other) > 0

    def __repr__(self):
        return '{0}{1}'.format(self.str_rank(), self._suit[0])

    def __str__(self):
        return '{0}{1}'.format(self.str_rank(), self._suit[0])

    def __hash__(self):
        return hash(self.__repr__())


class Deck:
    def __init__(self, non_standard_cards=None, shuffle=False):
        self._cards = standard_deck() if not non_standard_cards else non_standard_cards
        if shuffle:
            self.shuffle()

    def shuffle(self):
        random.shuffle(self._cards)

    def deal(self, num_players, cards_per_hand):
        dealt = [[] for _ in range(num_players)]
        for i in range(cards_per_hand):
            for j in range(num_players):
                dealt[j].append(self._cards.pop())
        return dealt

    def deal_one(self, num_cards):
        return [self._cards.pop() for _ in range(num_cards)]

    def cards_remaining(self):
        return len(self._cards)

    def next_card(self):
        return self._cards.pop(0)

    def random_card(self):
        card = random.choice(self._cards)
        self._cards.remove(card)
        return card

    def return_card(self, returned):
        self._cards.append(returned)

    def return_cards(self, returned):
        self._cards.extend(returned)

    def combinations_remaining(self, size):
        return itertools.combinations(self._cards, size)


def standard_deck():
    return [Card(r, s) for r in range(1, 14) for s in SUITS]


def split_suits(hand):
    return {suit: sorted([c for c in hand if c.suit == suit]) for suit in SUITS}


def split_ranks(hand):
    split = {}
    for c in hand:
        split[c.rank] = split.get(c.rank, [])
        split[c.rank].append(c)
    return split


def same_suit_runs(hand, min_run_size):
    results = []
    for suit, cards_for_suit in split_suits(hand).items():
        run_for_suit = []
        for c in cards_for_suit:
            if len(run_for_suit) == 0 or run_for_suit[len(run_for_suit) - 1].rank == c.rank - 1:
                run_for_suit.append(c)
        if len(run_for_suit) >= min_run_size:
            results.append(run_for_suit)
    return results


def is_run(hand, ace_high=False):
    hand = sorted(hand)
    if ace_high and hand[0].rank == 1:
        hand.append(hand.pop(0))

    for i in range(0, len(hand) - 1):
        if not hand[i].is_next_rank(hand[i + 1], ace_high):
            return False
    return True


def any_suit_runs(hand, min_run_size, remove_duplicates=True, ace_high=False):
    potential = []

    for i in range(min_run_size, len(hand) + 1):
        found_run_at_len_i = False
        for comb in itertools.combinations(hand, i):
            if is_run(comb, ace_high):
                potential.append(set(comb))
                found_run_at_len_i = True
        if not found_run_at_len_i:
            # no point checking longer runs if we didn't find any or the shorter ones
            break

    if not remove_duplicates:
        return sets_to_sorted_lists(potential)

    return sets_to_sorted_lists(remove_subsets(potential))


def same_suit_all_runs(hand, min_run_size):
    split = split_suits(hand)
    all_runs = []
    for same_suit in split.values():
        runs = any_suit_runs(same_suit, min_run_size, False)
        if runs:
            all_runs += runs
    return all_runs


def flushes(hand, min_flush_size):
    return [c for c in split_suits(hand).values() if len(c) >= min_flush_size]


def pairs(hand):
    return [list(comb) for comb in itertools.combinations(hand, 2)
            if comb[0].rank == comb[1].rank]


def three_of_a_kind(hand):
    return [list(comb) for comb in itertools.combinations(hand, 3)
            if comb[0].rank == comb[1].rank == comb[2].rank]


def four_of_a_kind(hand):
    return [list(comb) for comb in itertools.combinations(hand, 4)
            if comb[0].rank == comb[1].rank == comb[2].rank == comb[3].rank]


def hands_equal(*hands):
    base = set(hands[0])
    for h in hands[1:]:
        if set(h) != base:
            return False
    return True


if __name__ == '__main__':
    # cards = Card.from_str_list('1D, 2C, 3S')
    # print(is_run(cards))
    # cards = Card.from_str_list('JD, QC, KS')
    # print(is_run(cards))
    cards = Card.from_str_list('Ad, 2c, 3c')
    print(is_run(cards))
    print(is_run(cards, ace_high=True))

    print(hands_equal(Card.from_str_list('Ad, 2c, 3c'), Card.from_str_list('Ad, 2c, 3c')))
    print(hands_equal(Card.from_str_list('Ad, 2c, 3c'), Card.from_str_list('3c, Ad, 2c')))
    print(hands_equal(Card.from_str_list('Ad, 2c, 3c'), Card.from_str_list('Ad, 2c')))

    print(hands_equal(Card.from_str_list('Ad, 2c, 3c'),
                      Card.from_str_list('3c, Ad, 2c'),
                      Card.from_str_list('Ad, 3c, 2c')))

    print(hands_equal(Card.from_str_list('Ad, 2c, 3c'),
                      Card.from_str_list('3c, Ad, 2c'),
                      Card.from_str_list('Ad, 3c, 2h')))

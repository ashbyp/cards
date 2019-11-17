import random
import itertools
from cards.base.card import Card, standard_deck, pairs
from cards.base.player import Player
from cards.cribbage import score


class CribbagePlayer(Player):

    def choose_discards(self, hand, my_box):
        raise NotImplementedError()

    def next_pegging_card(self, stack, hand, turn_card):
        raise NotImplementedError()


def best_hand_ignore_box(hand, hand_size):
    best = []

    for comb in itertools.combinations(hand, hand_size):
        comb = list(comb)
        sc = score.score_hand(comb, None)
        if not best:
            best = [(sc, comb)]
        elif sc > best[0][0]:
            best = [(sc, comb)]
        elif sc == best[0][0]:
            best.append((sc, comb))

    return best


def best_hand_count_box(hand, hand_size, my_box):
    best = []

    for comb in itertools.combinations(hand, hand_size):
        comb = list(comb)
        box = [x for x in hand if x not in comb]
        sc = score.score_hand(comb, None)
        box_sc = 2 if (box[0].rank == box[1].rank or box[0].value + box[1].value == 15) else 0
        if my_box:
            sc += box_sc
        else:
            sc -= box_sc

        if not best:
            best = [(sc, comb, box)]
        elif sc > best[0][0]:
            best = [(sc, comb, box)]
        elif sc == best[0][0]:
            best.append((sc, comb, box))

    return best


def best_average_hand_ignore_box(hand, hand_size, deck):
    # for each possible set of 4 cards in the hand
    #   find score for each possible turn card
    #   average the scores
    #   choose hand with highest average
    # this method sucks in sim mode, ok for interactive

    possible_turns = [x for x in deck if x not in hand]
    hand_scores = []

    for comb in itertools.combinations(hand, hand_size):
        scores = []
        for turn in possible_turns:
            scores.append(score.score_hand(list(comb), turn))
        hand_scores.append((comb, scores))

    best_score = 0
    best_hand = None
    for comb, average_score in [(comb, sum(scores) / len(scores)) for comb, scores in hand_scores]:
        if average_score > best_score:
            best_score = average_score
            best_hand = comb

    return best_hand


def best_average_hand_count_box(hand, hand_size, deck, my_box):
    possible_turns = [x for x in deck if x not in hand]
    hand_scores = []

    for comb in itertools.combinations(hand, hand_size):
        box = [x for x in hand if x not in comb]
        box_sc = 2 if (box[0].rank == box[1].rank or box[0].value + box[1].value == 15) else 0
        scores = []
        for turn in possible_turns:
            hand_score = score.score_hand(list(comb), turn)
            if my_box:
                hand_score += box_sc
            else:
                hand_score -= box_sc
            scores.append(hand_score)
        hand_scores.append((comb, scores))

    best_score = 0
    best_hand = None
    for comb, average_score in [(comb, sum(scores) / len(scores)) for comb, scores in hand_scores]:
        if average_score > best_score:
            best_score = average_score
            best_hand = comb

    return best_hand


def best_peg_card(stack, hand):
    stack_score = sum([x.value for x in stack])
    score_per_card = []
    for card in hand:
        new_stack_score = stack_score + card.value
        bonus = 2 if new_stack_score in (15, 31) else 0
        if new_stack_score <= 31:
            score_per_card.append(bonus + score.score_pegging_stack(stack + [card])[0])
        else:
            score_per_card.append(None)

    if all(x is None for x in score_per_card):
        return None

    best_score = max(x for x in score_per_card if x is not None)

    for i, s in enumerate(score_per_card):
        if s == best_score:
            return hand[i]

    return None


def best_peg_card_skip_5s_and_21s(stack, hand):
    stack_score = sum([x.value for x in stack])
    score_per_card = []  # tuples (score, stack_score)
    for card in hand:
        new_stack_score = stack_score + card.value
        bonus = 2 if new_stack_score in (15, 31) else 0
        if new_stack_score <= 31:
            score_per_card.append((bonus + score.score_pegging_stack(stack + [card])[0], stack_score + card.value))
        else:
            score_per_card.append((None, None))

    if all(x[0] is None for x in score_per_card):
        return None

    best_score = max(x[0] for x in score_per_card if x[0] is not None)

    possible_plays = []

    for i, s in enumerate(score_per_card):
        if s[0] == best_score:
            possible_plays.append((s[1], hand[i]))

    if possible_plays:
        best_possible_plays = [x for x in possible_plays if x[0] not in (5, 21)]
        if best_possible_plays:
            return best_possible_plays[0][1]
        else:
            return possible_plays[0][1]

    return None


def best_peg_card_skip_5s_and_21s_no_runs(stack, hand):
    stack_score = sum([x.value for x in stack])
    score_per_card = []  # tuples (score, stack_score)
    for card in hand:
        new_stack_score = stack_score + card.value
        bonus = 2 if new_stack_score in (15, 31) else 0
        if new_stack_score <= 31:
            score_per_card.append((bonus + score.score_pegging_stack(stack + [card])[0], stack_score + card.value))
        else:
            score_per_card.append((None, None))

    if all(x[0] is None for x in score_per_card):
        return None

    best_score = max(x[0] for x in score_per_card if x[0] is not None)

    possible_plays = []

    for i, s in enumerate(score_per_card):
        if s[0] == best_score:
            possible_plays.append((s[1], hand[i]))

    def filter_runs(plays):
        if len(plays) == 1 or len(stack) == 0:
            return plays[0][1]

        for _, c in plays:
            if abs(c.rank - stack[-1].rank) > 2:
                return c

        return plays[0][1]

    if possible_plays:
        best_possible_plays = [x for x in possible_plays if x[0] not in (5, 21)]
        if best_possible_plays:
            return filter_runs(best_possible_plays)
        else:
            return filter_runs(possible_plays)

    return None


def handle_empty_stack(hand, turn_card):
    # this is too rigid if playing against a good player, but what we are doing is
    # - if we have a pair in our hand, we play one of the pair hoping the opponent has one so we can make 3-of-a-kind
    # - if we have a card matching the turn, we play it reducing changes of being paired by the opponent
    # - otherwise play our min card

    if not hand:
        return None

    if len(hand) == 1:
        return hand[0]

    if len(hand) > 2:
        pair_cards = pairs(hand)
        if pair_cards:
            return pair_cards[0][0]

    see_one_play_one = [x for x in hand if x.rank == turn_card.rank]
    if see_one_play_one:
        return see_one_play_one[0]

    return min(hand)


class DumbComputerPlayer(CribbagePlayer):
    # don't change the stupidity of this player, unit tests need it
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'Dumb_{DumbComputerPlayer.ME_COUNT}')
            DumbComputerPlayer.ME_COUNT += 1
        else:
            super().__init__(name)

    def choose_discards(self, hand, my_box):
        return hand[0:2]

    def next_pegging_card(self, stack, hand, turn_card):  #
        stack_score = sum([x.value for x in stack])
        for card in hand:
            if stack_score + card.value <= 31:
                return card
        return None

    def strategy(self):
        return "I will discard the first two cards dealt to me, and peg the first legal card in my hand"


class RandomComputerPlayer(CribbagePlayer):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'Random_{RandomComputerPlayer.ME_COUNT}')
            RandomComputerPlayer.ME_COUNT += 1
        else:
            super().__init__(name)

    def choose_discards(self, hand, my_box):
        return random.sample(hand, 2)

    def next_pegging_card(self, stack, hand, turn_card):  #
        stack_score = sum([x.value for x in stack])
        random.shuffle(hand)
        for card in hand:
            if stack_score + card.value <= 31:
                return card
        return None

    def strategy(self):
        return "I will discard two random cards, and play a random pegging card"


class HumanPlayer(CribbagePlayer):
    def __init__(self):
        name = input(' --> What is your name? ')
        super().__init__(name)
        self._strategy = input('\n --> What is your strategy? ') or 'Not declared'

    def choose_discards(self, hand, my_box):
        print(f'\n --> Your dealt cards are: {hand}')
        while True:
            try:
                user_input = None
                while not user_input:
                    user_input = input('\n --> What will you discard? ')
                cards = Card.from_str_list(user_input.replace(' ', ','))
                if set(cards).issubset(set(hand)):
                    if len(set(cards)) == 2:
                        return cards
                    else:
                        print(' --> Select two cards please, try again')
                else:
                    print(' --> Please select valid cards from your hand, try again')
            except ValueError as e:
                print(f' *** Input error "{e}"')

    def next_pegging_card(self, stack, hand, turn_card):
        if not hand:
            return None
        print(f'\n --> Your hand is {hand}')
        stack_total = sum([x.value for x in stack])
        go_allowed = (min([x.value for x in hand]) + stack_total) > 31
        while True:
            try:
                user_input = input('\n --> What will you peg next (return for GO)? ')
                if not user_input:
                    if go_allowed:
                        return None
                    else:
                        print(' *** GO not allowed, you can play')
                        continue
                card = Card.from_str(user_input)
                if card in hand:
                    if (card.value + stack_total) > 31:
                        print(' *** Total would be more than 31, try again')
                    else:
                        return card
                else:
                    print(f' *** You don\'t  have {card} in your hand')
            except ValueError as e:
                print(f' *** Input error "{e}"')

    def strategy(self):
        return self._strategy


class ComputerPlayerV1(CribbagePlayer):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'CompV1_{ComputerPlayerV1.ME_COUNT}')
            ComputerPlayerV1.ME_COUNT += 1
        else:
            super().__init__(name)

    def choose_discards(self, hand, my_box):
        best = best_hand_ignore_box(hand, 4)[0][1]
        return [x for x in hand if x not in best]

    def next_pegging_card(self, stack, hand, turn_card):
        return best_peg_card(stack, hand)

    def strategy(self):
        return "I will discard two cards that leave the best score in my hand, I will not consider the score of\n" +\
               " the cards thrown into the box or the turn card.  When pegging, I will play the card that gives\n" +\
               " me the best score, or if all equal, then a random card"


class ComputerPlayerV2(CribbagePlayer):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'CompV2_{ComputerPlayerV2.ME_COUNT}')
            ComputerPlayerV2.ME_COUNT += 1
        else:
            super().__init__(name)

    def choose_discards(self, hand, my_box):
        best = best_hand_ignore_box(hand, 4)[0][1]
        return [x for x in hand if x not in best]

    def next_pegging_card(self, stack, hand, turn_card):
        return best_peg_card_skip_5s_and_21s(stack, hand)

    def strategy(self):
        return "I will discard two cards that leave the best score in my hand, I will not consider the score of\n" +\
               " the cards thrown into the box or the turn card.  When pegging, I will play the card that gives\n" +\
               " me the best score, or if all equal, then a random car and will prefer not to leave a stack count\n" +\
               " of 5 or 21"


class ComputerPlayerV3(CribbagePlayer):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'CompV3_{ComputerPlayerV3.ME_COUNT}')
            ComputerPlayerV3.ME_COUNT += 1
        else:
            super().__init__(name)

    def choose_discards(self, hand, my_box):
        best = best_hand_count_box(hand, 4, my_box)[0][1]
        return [x for x in hand if x not in best]

    def next_pegging_card(self, stack, hand, turn_card):
        return best_peg_card_skip_5s_and_21s(stack, hand)

    def strategy(self):
        return "I will discard two cards that leave the best score in my hand, taking account of the score of\n" +\
               " the cards thrown into the box .  When pegging, I will play the card that gives\n" +\
               " me the best score, or if all equal, then a random car and will prefer not to leave a stack count\n" +\
               " of 5 or 21"


class ComputerPlayerV4(CribbagePlayer):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'CompV4_{ComputerPlayerV4.ME_COUNT}')
            ComputerPlayerV4.ME_COUNT += 1
        else:
            super().__init__(name)

        self._deck = standard_deck()

    def choose_discards(self, hand, my_box):
        best = best_average_hand_ignore_box(hand, 4, self._deck)
        return [x for x in hand if x not in best]

    def next_pegging_card(self, stack, hand, turn_card):
        return best_peg_card_skip_5s_and_21s(stack, hand)

    def strategy(self):
        return "I will evaluate all possible hands with all possible turn cards, and discard the two cards that\n" +\
                " gives me the highest average hand score, I will not consider the score of the cards thrown into\n" +\
                " the box.  When pegging, I will play the card that gives me the best score, or if all equal\n" +\
                " then a random card; and will prefer not to leave a stack count of 5 or 21"


class ComputerPlayerV5(CribbagePlayer):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'CompV5_{ComputerPlayerV5.ME_COUNT}')
            ComputerPlayerV5.ME_COUNT += 1
        else:
            super().__init__(name)

        self._deck = standard_deck()

    def choose_discards(self, hand, my_box):
        best = best_average_hand_count_box(hand, 4, self._deck, my_box)
        return [x for x in hand if x not in best]

    def next_pegging_card(self, stack, hand, turn_card):
        return best_peg_card_skip_5s_and_21s(stack, hand)

    def strategy(self):
        return "I will evaluate all possible hands with all possible turn cards, and discard the two cards that\n" +\
                " gives me the highest average hand score, I will add or subtract the discard score depending on\n" +\
                " whose deal it is. When pegging, I will play the card that gives me the best score, or if all \n" +\
                " equal then a random card; and will prefer not to leave a stack count of 5 or 21"


class ComputerPlayerV6(CribbagePlayer):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'CompV6_{ComputerPlayerV6.ME_COUNT}')
            ComputerPlayerV6.ME_COUNT += 1
        else:
            super().__init__(name)

        self._deck = standard_deck()

    def choose_discards(self, hand, my_box):
        best = best_average_hand_count_box(hand, 4, self._deck, my_box)
        return [x for x in hand if x not in best]

    def next_pegging_card(self, stack, hand, turn_card):
        return best_peg_card_skip_5s_and_21s_no_runs(stack, hand)

    def strategy(self):
        return "I will evaluate all possible hands with all possible turn cards, and discard the two cards that\n" +\
                " gives me the highest average hand score, I will add or subtract the discard score depending on\n" +\
                " whose deal it is. When pegging, I will play the card that gives me the best score, or if all \n" +\
                " equal then a random card; and will prefer not to leave a stack count of 5 or 21, or a potential \n" +\
                " run for my opponent"


class ComputerPlayerV7(CribbagePlayer):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'CompV7_{ComputerPlayerV7.ME_COUNT}')
            ComputerPlayerV7.ME_COUNT += 1
        else:
            super().__init__(name)

        self._deck = standard_deck()

    def choose_discards(self, hand, my_box):
        best = best_average_hand_count_box(hand, 4, self._deck, my_box)
        return [x for x in hand if x not in best]

    def next_pegging_card(self, stack, hand, turn_card):
        return best_peg_card_skip_5s_and_21s_no_runs(stack, hand) if stack else handle_empty_stack(hand, turn_card)

    def strategy(self):
        return "I will evaluate all possible hands with all possible turn cards, and discard the two cards that\n" +\
                " gives me the highest average hand score, I will add or subtract the discard score depending on\n" +\
                " whose deal it is. When pegging, I will play the card that gives me the best score, or if all \n" +\
                " equal then a random card; and will prefer not to leave a stack count of 5 or 21, or a potential \n" +\
                " run for my opponent.  When the stack is empty I will play a pair leader if I have a pair, else \n" + \
                " I'll play my lowest card"

# TODO
# Discard strategy that checks the average score for the box, with all possible turns


if __name__ == '__main__':
    p = ComputerPlayerV5()
    print(p.choose_discards(Card.from_str_list('ad,2d,3d,4d,6h,6d'), False))
    print(p.choose_discards(Card.from_str_list('ad,2d,3d,4d,6h,6d'), True))

import random
import itertools
from cards.base.card import Card, standard_deck
from cards.cribbage import score


class Player:
    def __init__(self, name):
        self._name = name
        self._score = 0

    @property
    def name(self):
        return self._name

    def choose_discards(self, hand, your_box):
        raise NotImplementedError()

    def next_pegging_card(self, stack, hand, turn_card):
        raise NotImplementedError()


class DumbComputerPlayer(Player):
    # don't change the stupidity of this player, unit tests need it
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'Dumb_{DumbComputerPlayer.ME_COUNT}')
            DumbComputerPlayer.ME_COUNT += 1
        else:
            super().__init__(name)

    def choose_discards(self, hand, your_box):
        return hand[0:2]

    def next_pegging_card(self, stack, hand, turn_card):  #
        stack_score = sum([x.value for x in stack])
        for card in hand:
            if stack_score + card.value <= 31:
                return card
        return None


class RandomComputerPlayer(Player):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'Random_{DumbComputerPlayer.ME_COUNT}')
            RandomComputerPlayer.ME_COUNT += 1
        else:
            super().__init__(name)

    def choose_discards(self, hand, your_box):
        return random.sample(hand, 2)

    def next_pegging_card(self, stack, hand, turn_card):  #
        stack_score = sum([x.value for x in stack])
        random.shuffle(hand)
        for card in hand:
            if stack_score + card.value <= 31:
                return card
        return None


class HumanPlayer(DumbComputerPlayer):  # for now
    def __init__(self):
        name = input('What is your name? ')
        super().__init__(name)

    def choose_discards(self, hand, your_box):
        print(f'\nYour dealt cards are: {hand}')
        while True:
            try:
                user_input = None
                while not user_input:
                    user_input = input('\nWhat will you discard? ')
                cards = Card.from_str_list(user_input)
                if set(cards).issubset(set(hand)):
                    if len(set(cards)) == 2:
                        return cards
                    else:
                        print('Select two cards please, try again')
                else:
                    print('Please select valid cards from your hand, try again')
            except ValueError as e:
                print(f'Input error "{e}"')

    def next_pegging_card(self, stack, hand, turn_card):
        if not hand:
            return None
        print(f'\nYour hand is {hand}')
        stack_total = sum([x.value for x in stack])
        go_allowed = (min([x.value for x in hand]) + stack_total) > 31
        while True:
            try:
                user_input = input('\nWhat will you peg next (return for GO)? ')
                if not user_input:
                    if go_allowed:
                        return None
                    else:
                        print('GO not allowed, you can play')
                        continue
                card = Card.from_str(user_input)
                if card in hand:
                    if (card.value + stack_total) > 31:
                        print('Total would be more than 31, try again')
                    else:
                        return card
                else:
                    print('Selection is not a subset of your cards, try again')
            except ValueError as e:
                print(f'Input error "{e}"')


class ComputerPlayerV1(Player):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'CompV1_{ComputerPlayerV1.ME_COUNT}')
            ComputerPlayerV1.ME_COUNT += 1
        else:
            super().__init__(name)

    def choose_discards(self, hand, your_box):
        best = score.choose_best_hand(hand, 4)[0][1]
        return [x for x in hand if x not in best]

    def next_pegging_card(self, stack, hand, turn_card):
        stack_score = sum([x.value for x in stack])
        score_per_card = []
        for card in hand:
            if stack_score + card.value <= 31:
                score_per_card.append(score.score_pegging_stack(stack + [card])[0])
            else:
                score_per_card.append(None)

        if all(x is None for x in score_per_card):
            return None

        best_score = max(x for x in score_per_card if x is not None)

        for i, s in enumerate(score_per_card):
            if s == best_score:
                return hand[i]

        return None


class ComputerPlayerV2(ComputerPlayerV1):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'CompV2_{ComputerPlayerV2.ME_COUNT}')
            ComputerPlayerV2.ME_COUNT += 1
        else:
            super().__init__(name)

    def next_pegging_card(self, stack, hand, turn_card):
        stack_score = sum([x.value for x in stack])
        score_per_card = []  # tuples (score, stack_score)
        for card in hand:
            if stack_score + card.value <= 31:
                score_per_card.append((score.score_pegging_stack(stack + [card])[0], stack_score + card.value))
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


class ComputerPlayerV3(ComputerPlayerV2):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'CompV3_{ComputerPlayerV3.ME_COUNT}')
            ComputerPlayerV3.ME_COUNT += 1
        else:
            super().__init__(name)

        self._deck = standard_deck()

    def choose_discards(self, hand, your_box):
        # for each possible set of 4 cards in the hand
        #   find score for each possible turn card
        #   average the scores
        #   choose hand with highest average
        # this method sucks in sim mode, ok for interactive

        possible_turns = [x for x in self._deck if x not in hand]
        hand_scores = []

        for comb in itertools.combinations(hand, 4):
            scores = []
            for turn in possible_turns:
                scores.append(score.score_hand(list(comb), turn))
            hand_scores.append((comb, scores))

        best_score = 0
        best_hand = None
        for comb, average_score in [(comb, sum(scores)/len(scores)) for comb, scores in hand_scores]:
            if average_score > best_score:
                best_score = average_score
                best_hand = comb

        return [x for x in hand if x not in best_hand]


class ComputerPlayerV4(ComputerPlayerV3):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'CompV4_{ComputerPlayerV4.ME_COUNT}')
            ComputerPlayerV4.ME_COUNT += 1
        else:
            super().__init__(name)

    def next_pegging_card(self, stack, hand, turn_card):
        # TODO
        # same as parent but try to avoid leaving runs
        return super().next_pegging_card(stack, hand, turn_card)
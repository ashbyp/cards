from cards.ginrummy import score


class Player:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def new_hand(self, hand):
        # new 10 cards
        raise NotImplementedError()

    def pass_turn(self, stack, face_up_card):
        # non dealer gets a chance to pass, dealer also gets a chance to pass if the non-dealer passes
        raise NotImplementedError()

    def take_face_up(self, face_up):
        # return true to take the face up card else false to get the top of the stack
        raise NotImplementedError()

    def next_card_and_discard(self, card):
        # your next card, return you discard after deciding what to do with the new card.
        # If None is returned it is assumed you have BIG GIN
        raise NotImplementedError()

    def knock(self):
        # do you want to knock
        raise NotImplementedError()

    def get_hand(self):
        # return your hand
        raise NotImplementedError()

    def strategy(self):
        raise NotImplementedError()


class DumbComputerPlayer(Player):
    ME_COUNT = 1

    def __init__(self, name=None):
        if not name:
            super().__init__(f'Dumb_{DumbComputerPlayer.ME_COUNT}')
            DumbComputerPlayer.ME_COUNT += 1
        else:
            super().__init__(name)
        self._hand = None

    def new_hand(self, hand):
        self._hand = hand

    def pass_turn(self, stack, face_up_card):
        return False

    def take_face_up(self, face_up):
        return False

    def next_card_and_discard(self, card):
        self._hand.append(card)
        return self._hand.pop(0)

    def knock(self):
        sequences, dead_wood_count = score.score_hand(self._hand)
        return dead_wood_count <= 10

    def get_hand(self):
        return self._hand

    def strategy(self):
        return \
            "I will always take from the top of the stack, and discard on a FIFO basis, I will knock\n" +\
            " as soon as I am allowed to do so"





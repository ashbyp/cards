from cards.ginrummy import score
from cards.base.player import Player


class RummyPlayer(Player):

    def new_hand(self, hand):
        raise NotImplementedError()

    def dealer_pass(self, face_up_card):
        # return true to pass or false to take the face up card
        raise NotImplementedError()

    def non_dealer_pass(self, face_up_card):
        # return true pass or false to take the face up card
        raise NotImplementedError()

    def take_face_up(self, card):
        # return true to take the face up card else false and you'll get the stack card
        raise NotImplementedError()

    def next_turn(self, card):
        # return your discard (or if you have big gin return None)
        pass

    def ready_to_knock(self):
        # do you want to knock?
        raise NotImplementedError()

    def opponent_action(self, took_discard, discard):
        # if your opponent took your last discard, took_discard will be true
        raise NotImplementedError()

    def declare_hand(self):
        # declare your hand, which is a list of melds and your dead wood count
        raise NotImplementedError()


class DumbComputerPlayer(RummyPlayer):
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

    def dealer_pass(self, face_up_card):
        # return true to pass or false to take the face up card
        return False

    def non_dealer_pass(self, face_up_card):
        # return true pass or false to take the face up card
        return False

    def take_face_up(self, card):
        # return true to take the face up card else false and you'll get the stack card
        return False

    def next_turn(self, card):
        # return your discard (or if you have big gin return None)
        return card

    def ready_to_knock(self):
        # do you want to knock?
        raise NotImplementedError()

    def declare_hand(self):
        # declare your hand, which is a list of melds and your dead wood count
        raise NotImplementedError()

    def opponent_action(self, took_discard, discard):
        pass

    def strategy(self):
        return \
            "I will always take from the top of the stack, and discard on a FIFO basis, I will knock\n" +\
            " as soon as I am allowed to do so"





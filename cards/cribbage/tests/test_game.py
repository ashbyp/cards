from unittest import TestCase

from cards.base import card
from cards.cribbage import player, game, display


class TestGame(TestCase):

    def setUp(self):
        self._p1 = player.DumbComputerPlayer('p1')
        self._p2 = player.DumbComputerPlayer('p2')
        self._game = game.Game(self._p1, self._p2, 121, display=display.Display(False), trace_enabled=False)
        self._board = game.Board(self._p1, self._p2, 121)

    def test_decide_dealer(self):
        deck = card.Deck()
        deck.shuffle()
        for _ in range(100):
            dealer, non_dealer, dealer_card, non_dealer_card = self._game.decide_dealer(deck)
            self.assertTrue(dealer_card < non_dealer_card)
            self.assertEqual(52, deck.cards_remaining())

    def test_discard(self):
        deck = card.Deck()
        hands = deck.deal(2, 6)
        dealer_hand, non_dealer_hand, box = self._game.discard(self._p1, self._p2, hands[0], hands[1])
        self.assertEqual(4, len(dealer_hand))
        self.assertEqual(4, len(non_dealer_hand))
        self.assertEqual(4, len(box))
        self.assertTrue(all([x not in dealer_hand and x not in non_dealer_hand for x in box]))

    def test_turn(self):
        deck = card.Deck()
        turn_card = self._game.turn(deck, self._p1, self._board)
        self.assertTrue(turn_card is not None)
        deck = card.Deck([card.Card('11', 'H')])
        turn_card = self._game.turn(deck, self._p1, self._board)
        self.assertEqual(card.Card('11', 'H'), turn_card)
        self.assertEqual(2, self._board.player_score(self._p1))

    def test_play_pegging_card_empty_stack(self):
        stack = []
        hand = card.Card.from_str_list('QS, JD, 6C, 2H')
        turn = card.Card.from_str('3C')

        go = self._game.play_pegging_card(self._p1, stack, hand, turn, self._board)

        self.assertEqual(1, len(stack))
        self.assertEqual(card.Card.from_str('QS'), stack[0])
        self.assertEqual(0, self._board.player_score(self._p1))
        self.assertFalse(go)

    def test_play_pegging_card_15(self):
        stack = card.Card.from_str_list('10C')
        hand = card.Card.from_str_list('5d, JD, 6C, 2H')
        turn = card.Card.from_str('3C')

        go = self._game.play_pegging_card(self._p1, stack, hand, turn, self._board)

        self.assertEqual(2, len(stack))
        self.assertEqual(card.Card.from_str('5d'), stack[1])
        self.assertEqual(2, self._board.player_score(self._p1))
        self.assertFalse(go)

    def test_play_pegging_card_31(self):
        stack = card.Card.from_str_list('10C,10D,10S')
        hand = card.Card.from_str_list('AS, JD, 6C, 2H')
        turn = card.Card.from_str('3C')

        self.assertEqual(3, len(stack))

        go = self._game.play_pegging_card(self._p1, stack, hand, turn, self._board)

        self.assertEqual(4, len(stack))
        self.assertEqual(card.Card.from_str('AS'), stack[3])
        self.assertEqual(2, self._board.player_score(self._p1))
        self.assertFalse(go)

    def test_play_pegging_card_GO(self):
        stack = card.Card.from_str_list('10C,10D,10S')
        hand = card.Card.from_str_list('JD, 6C, 2H')
        turn = card.Card.from_str('3C')

        self.assertEqual(3, len(stack))

        go = self._game.play_pegging_card(self._p1, stack, hand, turn, self._board)

        self.assertEqual(3, len(stack))
        self.assertEqual(0, self._board.player_score(self._p1))
        self.assertTrue(go)

    def test_play_pegging_card_game_won(self):
        self._board.add_points(self._p1, 120)
        stack = card.Card.from_str_list('10C,10D,10S')
        hand = card.Card.from_str_list('AC, 6C, 2H')
        turn = card.Card.from_str('3C')

        with self.assertRaises(game.GameWonException):
            self._game.play_pegging_card(self._p1, stack, hand, turn, self._board)

        self.assertEqual(122, self._board.player_score(self._p1))

    def test_pegging_score_31(self):
        dealer = card.Card.from_str_list('AD, 3D, 5D, 7S')
        non_dealer = card.Card.from_str_list('QH, 10H, 7H, 5C')

        self._game.pegging(self._p1, self._p2, dealer, non_dealer, card.Card.from_str('KC'), self._board)

        #  QH, AD, 10H, 3D, 7H = 31 scored by non_dealer 2+1 points
        #  5D 5C 7S = pair for non dealer 2, last card for dealer, 1 point

        self.assertEqual(1, self._board.player_score(self._p1))
        self.assertEqual(4, self._board.player_score(self._p2))

    def test_pegging_score_15(self):
        dealer = card.Card.from_str_list('5D, 3D, 8D, 7S')
        non_dealer = card.Card.from_str_list('QH, 10H, 7H, 5C')

        self._game.pegging(self._p1, self._p2, dealer, non_dealer, card.Card.from_str('KC'), self._board)

        # QH 5D (dealer scores 2) 10H 3D last card for dealer, dealer total 3 points
        # 7H 8D (dealer scores 2) 5C 7S last card for dealer, dealer total 3 points

        self.assertEqual(6, self._board.player_score(self._p1))
        self.assertEqual(0, self._board.player_score(self._p2))

    def test_lots_of_games(self):
        for i in range(100):
            self.assertEqual(0, self._board.player_score(self._p1))
            self.assertEqual(0, self._board.player_score(self._p2))
            self._game.play(board=self._board)
            self.assertTrue(self._board.player_score(self._p1) >= 121 or self._board.player_score(self._p2) >= 121)
            self._board.reset()



from unittest import TestCase
from functools import reduce

from cards.cribbage.player import DumbComputerPlayer
from cards.cribbage.stats import Collector
from cards.cribbage.game import Game
from cards.cribbage.display import Display
from cards.cribbage.board import Board
from cards.base.card import Card


class TestStats(TestCase):

    def setUp(self):
        self._p1 = DumbComputerPlayer('p1')
        self._p2 = DumbComputerPlayer('p2')
        self._collector = Collector(self._p1, self._p2)
        self._board = Board(self._p1, self._p2, 121)
        self._game = Game(self._p1, self._p2, 121, display=Display(False), stats=self._collector)

    def test_constructor(self):
        self.assertEqual((0, 0, 0), self._collector.averages(self._p1))
        self.assertEqual((0, 0, 0), self._collector.averages(self._p2))

    def test_pegging_basic(self):
        self._collector.add_pegging_score(self._p1, 4)
        self._collector.add_pegging_score(self._p1, 6)
        self._collector.add_pegging_score(self._p1, 8)
        self.assertEqual((6, 0, 0), self._collector.averages(self._p1))
        self._collector.add_pegging_score(self._p2, 1)
        self._collector.add_pegging_score(self._p2, 2)
        self._collector.add_pegging_score(self._p2, 3)
        self.assertEqual((2, 0, 0), self._collector.averages(self._p2))

    def test_hand_basic(self):
        self._collector.add_hand_score(self._p1, 4)
        self._collector.add_hand_score(self._p1, 6)
        self._collector.add_hand_score(self._p1, 8)
        self.assertEqual((0, 6, 0), self._collector.averages(self._p1))
        self._collector.add_hand_score(self._p2, 1)
        self._collector.add_hand_score(self._p2, 2)
        self._collector.add_hand_score(self._p2, 3)
        self.assertEqual((0, 2, 0), self._collector.averages(self._p2))

    def test_box_basic(self):
        self._collector.add_box_score(self._p1, 4)
        self._collector.add_box_score(self._p1, 6)
        self._collector.add_box_score(self._p1, 8)
        self.assertEqual((0, 0, 6), self._collector.averages(self._p1))
        self._collector.add_box_score(self._p2, 1)
        self._collector.add_box_score(self._p2, 2)
        self._collector.add_box_score(self._p2, 3)
        self.assertEqual((0, 0, 2), self._collector.averages(self._p2))

    def test_pegging(self):
        dealer = Card.from_str_list('AD, 3D, 5D, 7S')
        non_dealer = Card.from_str_list('QH, 10H, 7H, 5C')

        self._game.pegging(self._p1, self._p2, dealer, non_dealer, Card.from_str('KC'), self._board)

        #  QH, AD, 10H, 3D, 7H = 31 scored by non_dealer 2+1 points
        #  5D 5C 7S = pair for non dealer 2, last card for dealer, 1 point

        self.assertEqual((1, 0, 0), self._collector.averages(self._p1))
        self.assertEqual((4, 0, 0), self._collector.averages(self._p2))

    def test_reduce(self):
        c1 = Collector(self._p1, self._p2)
        c2 = Collector(self._p1, self._p2)
        c1.add_pegging_score(self._p1, 3)
        c2.add_pegging_score(self._p1, 4)
        c1.add_hand_score(self._p1, 10)
        c2.add_hand_score(self._p1, 11)
        c1.add_box_score(self._p1, 8)
        c2.add_box_score(self._p1, 9)

        self.assertEqual((3, 10, 8), c1.averages(self._p1))
        self.assertEqual((4, 11, 9), c2.averages(self._p1))

        r = reduce(lambda x, y: ((x[0]+y[0])/2, (x[1]+y[1])/2, (x[2]+y[2])/2), [x.averages(self._p1) for x in (c1, c2)])
        self.assertEqual((3.5, 10.5, 8.5), r)
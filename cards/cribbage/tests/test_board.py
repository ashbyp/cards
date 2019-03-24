from unittest import TestCase
from cards.cribbage.player import DumbComputerPlayer
from cards.cribbage.board import Board, GameWonException


class TestBoard(TestCase):

    def setUp(self):
        self._p1 = DumbComputerPlayer('p1')
        self._p2 = DumbComputerPlayer('p2')

    def test_CribBoard_constructor(self):
        board = Board(self._p1, self._p2)
        self.assertEqual(0, board.player_score(self._p1))
        self.assertEqual(0, board.player_score(self._p2))
        self.assertEqual('p1: 0, p2: 0', str(board))

    def test_CribBoard_pegging(self):
        board = Board(self._p1, self._p2)
        board.add_points(self._p1, 10)
        board.add_points(self._p1, 12)
        board.add_points(self._p2, 3)
        board.add_points(self._p2, 2)
        self.assertEqual(22, board.player_score(self._p1))
        self.assertEqual(5, board.player_score(self._p2))
        self.assertEqual('p1: 22, p2: 5', str(board))

    def test_CribBoard_player1_wins(self):
        board = Board(self._p1, self._p2)
        board.add_points(self._p1, 10)
        with self.assertRaises(GameWonException):
            board.add_points(self._p1, 112)
        self.assertEqual(122, board.player_score(self._p1))

    def test_CribBoard_player2_wins(self):
        board = Board(self._p1, self._p2)
        board.add_points(self._p2, 10)
        with self.assertRaises(GameWonException):
            board.add_points(self._p2, 112)
        self.assertEqual(122, board.player_score(self._p2))

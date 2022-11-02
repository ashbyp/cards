from collections import OrderedDict


class Board:

    def __init__(self, player1, player2, target_points=100):
        self._board = OrderedDict({
            player1: {'score': 0, 'boxes': 0},
            player2: {'score': 0, 'boxes': 0},
        })
        self._target_points = target_points

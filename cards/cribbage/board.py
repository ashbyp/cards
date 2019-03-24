from collections import OrderedDict


class GameWonException(Exception):
    def __init__(self, winning_player, winning_player_score):
        super().__init__(f'{winning_player.name} won with {winning_player_score}')
        self._winning_player = winning_player


class Board:

    def __init__(self, player1, player2, target_points=121):
        self._board = OrderedDict({
            player1: {'front': 0, 'back': 0},
            player2: {'front': 0, 'back': 0},
        })
        self._target_points = target_points

    def add_points(self, player, points):
        self._board[player]['back'] = self._board[player]['front']
        self._board[player]['front'] = self._board[player]['front'] + points
        if self._board[player]['front'] >= self._target_points:
            raise GameWonException(player, self._board[player]['front'])

    def player_score(self, pl):
        return self._board[pl]['front']

    def reset(self):
        for _, player in self._board.items():
            player['front'] = 0
            player['back'] = 0

    def __str__(self):
        keys = list(self._board.keys())
        return f'{keys[0].name}: {self.player_score(keys[0])}, {keys[1].name}: {self.player_score(keys[1])}'

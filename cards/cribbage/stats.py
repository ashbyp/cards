import numpy as np
from collections import OrderedDict
from cards.cribbage.player import Player


class Collector:

    def __init__(self, p1, p2):
        self.stats = OrderedDict({
            p1.name: {'pegging': [], 'hand': [], 'box': []},
            p2.name: {'pegging': [], 'hand': [], 'box': []},
        })

    def add_pegging_score(self, player, score):
        self.stats[player.name]['pegging'].append(score)

    def add_hand_score(self, player, score):
        self.stats[player.name]['hand'].append(score)

    def add_box_score(self, player, score):
        self.stats[player.name]['box'].append(score)
        
    def averages(self, player):
        player_name = player.name if isinstance(player, Player) else player

        pegging = self.stats[player_name]['pegging']
        hand = self.stats[player_name]['hand']
        box = self.stats[player_name]['box']

        avg_peg = np.mean(pegging) if pegging else 0
        avg_hand = np.mean(hand) if hand else 0
        avg_box = np.mean(box) if box else 0

        return avg_peg, avg_hand, avg_box

    def rating(self, player):
        return sum(self.averages(player))

    def _averages_tostring(self, player_name):
        averages = self.averages(player_name)
        overall = sum(averages)
        return f'{player_name}: avg peg %.2f avg hand %.2f avg box %.2f overall %.2f' % (*averages, overall)

    def __str__(self):
        return str([self._averages_tostring(k) for k in self.stats])

    @classmethod
    def combine(cls, collectors, p1, p2):
        combined = Collector(p1, p2)
        for collector in collectors:
            combined.stats[p1.name]['pegging'] += collector.stats[p1.name]['pegging']
            combined.stats[p1.name]['hand'] += collector.stats[p1.name]['hand']
            combined.stats[p1.name]['box'] += collector.stats[p1.name]['box']
            combined.stats[p2.name]['pegging'] += collector.stats[p2.name]['pegging']
            combined.stats[p2.name]['hand'] += collector.stats[p2.name]['hand']
            combined.stats[p2.name]['box'] += collector.stats[p2.name]['box']
        return combined


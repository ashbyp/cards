

class Collector:

    def __init__(self, p1, p2):
        self._stats = {
            p1: {'pegging': [], 'hand': [], 'box': []},
            p2: {'pegging': [], 'hand': [], 'box': []},
        }

    def add_pegging_score(self, player, score):
        self._stats[player]['pegging'].append(score)

    def add_hand_score(self, player, score):
        self._stats[player]['hand'].append(score)

    def add_box_score(self, player, score):
        self._stats[player]['box'].append(score)

    def averages(self, player):
        pegging = self._stats[player]['pegging']
        hand = self._stats[player]['hand']
        box = self._stats[player]['box']

        avg_peg = sum(pegging) / len(pegging) if pegging else 0
        avg_hand = sum(hand) / len(hand) if hand else 0
        avg_box = sum(box) / len(box) if box else 0

        return avg_peg, avg_hand, avg_box

    def averages_tostring(self, player):
        averages = self.averages(player)
        overall = sum(averages)
        return f'{player.name}: avg peg %.2f avg hand %.2f avg box %.2f overall %.2f' % (*averages, overall)

    def __str__(self):
        return str([self.averages_tostring(k) for k in self._stats])


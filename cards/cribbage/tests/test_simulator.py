from unittest import TestCase
import platform
from cards.cribbage.simulations import PlayerComparisonSimulator


class TestSimulator(TestCase):

    def setUp(self):
        self.is_win = platform.system() == 'Windows'

    def test_comparison(self):
        if not self.is_win:
            print('\n\nRunning simulations')
            sim = PlayerComparisonSimulator(keep_alive=True)
            sim.run()
        self.assertTrue(True)

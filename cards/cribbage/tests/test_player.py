from unittest import TestCase
from cards.cribbage.player import choose_best_hand, choose_best_hand_ignore_box
from cards.base.card import Card


class TestPlayer(TestCase):

    def test_choose_best_hand_ignore_box_single_match(self):
        best = choose_best_hand_ignore_box(Card.from_str_list('2d, 3d, 4d, 5d, 9c, 9s'), 4)
        self.assertEqual(1, len(best))
        self.assertEqual(8, best[0][0])
        self.assertTrue(set(Card.from_str_list('2d, 3d, 4d, 5d')) in [set(x[1]) for x in best])

    def test_choose_best_hand_ignore_box_multiple_matches(self):
        best = choose_best_hand_ignore_box(Card.from_str_list('ac,2c,9c,7c,3s,kd'), 4)
        self.assertEqual(2, len(best))
        self.assertEqual(5, best[0][0])
        self.assertTrue(set(Card.from_str_list('AC,2C,9C,3S')) in [set(x[1]) for x in best])
        self.assertTrue(set(Card.from_str_list('AC, 2C, 3S, KD')) in [set(x[1]) for x in best])

    def test_choose_best_hand_single_match_my_box(self):
        best = choose_best_hand(Card.from_str_list('2d, 3d, 4d, 5d, 9c, 9s'), 4, True)
        self.assertEqual(1, len(best))
        self.assertEqual(10, best[0][0])
        self.assertTrue(set(Card.from_str_list('2d, 3d, 4d, 5d')) in [set(x[1]) for x in best])

    def test_choose_best_hand_single_match_your_box(self):
        best = choose_best_hand(Card.from_str_list('2d, 3d, 4d, 5d, 8c, 9s'), 4, False)
        self.assertEqual(1, len(best))
        self.assertEqual(8, best[0][0])
        self.assertTrue(set(Card.from_str_list('2d, 3d, 4d, 5d')) in [set(x[1]) for x in best])

    def test_choose_best_hand_multiple_matches_my_box(self):
        best = choose_best_hand(Card.from_str_list('4d, 4s, 6d, 6s, 10h, 10s'), 4, True)
        self.assertEqual(3, len(best))
        self.assertEqual(6, best[0][0])
        self.assertTrue(set(Card.from_str_list('4D, 4S, 6D, 6S')) in [set(x[1]) for x in best])

    def test_choose_best_hand_multiple_matches_your_box(self):
        best = choose_best_hand(Card.from_str_list('4d, 4s, 6d, 6s, 10h, 10s'), 4, False)
        self.assertEqual(15, len(best))
        self.assertEqual(2, best[0][0])
        self.assertTrue(set(Card.from_str_list('4D, 4S, 6D, 6S')) in [set(x[1]) for x in best])




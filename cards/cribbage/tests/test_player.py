from unittest import TestCase
from cards.cribbage import player
from cards.base.card import Card


class TestPlayer(TestCase):

    def test_best_hand_ignore_box_single_match(self):
        best = player.best_hand_ignore_box(Card.from_str_list('2d, 3d, 4d, 5d, 9c, 9s'), 4)
        self.assertEqual(1, len(best))
        self.assertEqual(8, best[0][0])
        self.assertTrue(set(Card.from_str_list('2d, 3d, 4d, 5d')) in [set(x[1]) for x in best])

    def test_best_hand_ignore_box_multiple_matches(self):
        best = player.best_hand_ignore_box(Card.from_str_list('ac,2c,9c,7c,3s,kd'), 4)
        self.assertEqual(2, len(best))
        self.assertEqual(5, best[0][0])
        self.assertTrue(set(Card.from_str_list('AC,2C,9C,3S')) in [set(x[1]) for x in best])
        self.assertTrue(set(Card.from_str_list('AC, 2C, 3S, KD')) in [set(x[1]) for x in best])

    def test_best_hand_single_match_my_box(self):
        best = player.best_hand_count_box(Card.from_str_list('2d, 3d, 4d, 5d, 9c, 9s'), 4, True)
        self.assertEqual(1, len(best))
        self.assertEqual(10, best[0][0])
        self.assertTrue(set(Card.from_str_list('2d, 3d, 4d, 5d')) in [set(x[1]) for x in best])

    def test_best_hand_single_match_your_box(self):
        best = player.best_hand_count_box(Card.from_str_list('2d, 3d, 4d, 5d, 8c, 9s'), 4, False)
        self.assertEqual(1, len(best))
        self.assertEqual(8, best[0][0])
        self.assertTrue(set(Card.from_str_list('2d, 3d, 4d, 5d')) in [set(x[1]) for x in best])

    def test_best_hand_multiple_matches_my_box(self):
        best = player.best_hand_count_box(Card.from_str_list('4d, 4s, 6d, 6s, 10h, 10s'), 4, True)
        self.assertEqual(3, len(best))
        self.assertEqual(6, best[0][0])
        self.assertTrue(set(Card.from_str_list('4D, 4S, 6D, 6S')) in [set(x[1]) for x in best])

    def test_best_hand_multiple_matches_your_box(self):
        best = player.best_hand_count_box(Card.from_str_list('4d, 4s, 6d, 6s, 10h, 10s'), 4, False)
        self.assertEqual(15, len(best))
        self.assertEqual(2, best[0][0])
        self.assertTrue(set(Card.from_str_list('4D, 4S, 6D, 6S')) in [set(x[1]) for x in best])

    def test_best_peg_card_empty_stack(self):
        stack = Card.from_str_list('')
        hand = Card.from_str_list('5c, 3c,7s,jd')
        pegging_card = player.best_peg_card(stack, hand)
        self.assertEqual(Card.from_str('5c'), pegging_card)

    def test_best_peg_card_hit_15(self):
        stack = Card.from_str_list('8c')
        hand = Card.from_str_list('5c, 3c,7s,jd')
        pegging_card = player.best_peg_card(stack, hand)
        self.assertEqual(Card.from_str('7s'), pegging_card)

    def test_best_peg_card_hit_31(self):
        stack = Card.from_str_list('8c,8d,5s')
        hand = Card.from_str_list('3c,7s,jd')
        pegging_card = player.best_peg_card(stack, hand)
        self.assertEqual(Card.from_str('jd'), pegging_card)

    def test_best_peg_card_hit_pair(self):
        stack = Card.from_str_list('8c')
        hand = Card.from_str_list('5c, 8h,7s,jd')
        pegging_card = player.best_peg_card(stack, hand)
        self.assertEqual(Card.from_str('8h'), pegging_card)

    def test_best_peg_card_hit_run(self):
        stack = Card.from_str_list('8c,6d')
        hand = Card.from_str_list('3c,7s,jd')
        pegging_card = player.best_peg_card(stack, hand)
        self.assertEqual(Card.from_str('7s'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_empty_stack(self):
        stack = Card.from_str_list('')
        hand = Card.from_str_list('3c,7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s(stack, hand)
        self.assertEqual(Card.from_str('3c'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_empty_stack_skip5(self):
        stack = Card.from_str_list('')
        hand = Card.from_str_list('5c, 7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s(stack, hand)
        self.assertEqual(Card.from_str('7s'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_skip21(self):
        stack = Card.from_str_list('10d,6s')
        hand = Card.from_str_list('5c, 7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s(stack, hand)
        self.assertEqual(Card.from_str('7s'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_hit_15(self):
        stack = Card.from_str_list('8c')
        hand = Card.from_str_list('5c, 3c,7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s(stack, hand)
        self.assertEqual(Card.from_str('7s'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_hit_31(self):
        stack = Card.from_str_list('8c,8d,5s')
        hand = Card.from_str_list('3c,7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s(stack, hand)
        self.assertEqual(Card.from_str('jd'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_hit_pair(self):
        stack = Card.from_str_list('8c')
        hand = Card.from_str_list('5c, 8h,7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s(stack, hand)
        self.assertEqual(Card.from_str('8h'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_hit_run(self):
        stack = Card.from_str_list('8c,6d')
        hand = Card.from_str_list('3c,7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s(stack, hand)
        self.assertEqual(Card.from_str('7s'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_no_runs_empty_stack(self):
        stack = Card.from_str_list('')
        hand = Card.from_str_list('3c,7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s_no_runs(stack, hand)
        self.assertEqual(Card.from_str('3c'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_no_runs_empty_stack_skip5(self):
        stack = Card.from_str_list('')
        hand = Card.from_str_list('5c, 7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s_no_runs(stack, hand)
        self.assertEqual(Card.from_str('7s'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_no_runs_skip21(self):
        stack = Card.from_str_list('10d,6s')
        hand = Card.from_str_list('5c,ks,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s_no_runs(stack, hand)
        self.assertEqual(Card.from_str('ks'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_no_runs_hit_15(self):
        stack = Card.from_str_list('8c')
        hand = Card.from_str_list('5c, 3c,7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s_no_runs(stack, hand)
        self.assertEqual(Card.from_str('7s'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_no_runs_hit_31(self):
        stack = Card.from_str_list('8c,8d,5s')
        hand = Card.from_str_list('3c,7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s_no_runs(stack, hand)
        self.assertEqual(Card.from_str('jd'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_no_runs_hit_pair(self):
        stack = Card.from_str_list('8c')
        hand = Card.from_str_list('5c, 8h,7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s_no_runs(stack, hand)
        self.assertEqual(Card.from_str('8h'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_no_runs_hit_run(self):
        stack = Card.from_str_list('8c,6d')
        hand = Card.from_str_list('3c,7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s_no_runs(stack, hand)
        self.assertEqual(Card.from_str('7s'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_no_runs_slip_run1(self):
        stack = Card.from_str_list('3c')
        hand = Card.from_str_list('4s,2c,7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s_no_runs(stack, hand)
        self.assertEqual(Card.from_str('7s'), pegging_card)

    def test_best_peg_cards_skip_5s_and_21s_no_runs_slip_run2(self):
        stack = Card.from_str_list('3c')
        hand = Card.from_str_list('5s,2c,7s,jd')
        pegging_card = player.best_peg_cards_skip_5s_and_21s_no_runs(stack, hand)
        self.assertEqual(Card.from_str('7s'), pegging_card)




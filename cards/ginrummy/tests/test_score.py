from unittest import TestCase
from cards.ginrummy import score
from cards.base.card import Card


class TestScore(TestCase):

    def test_find_melds_three_of_kind(self):
        hand = Card.from_str_list('2c,2d,3s,5c,6d,7h,8s,9c,10d,jc')
        self.assertFalse(score.find_all_melds(hand))
        hand = Card.from_str_list('2c,2d,2s,5c,6d,7h,8s,9c,10d,jc')
        self.assertEqual([Card.from_str_list('2c,2d,2s')], score.find_all_melds(hand))
        hand = Card.from_str_list('2c,2d,2s,5c,5d,5h,8s,9c,10d,jc')
        self.assertEqual([Card.from_str_list('2c,2d,2s'), Card.from_str_list('5c,5d,5h')], score.find_all_melds(hand))

    def test_find_melds_four_of_kind(self):
        hand = Card.from_str_list('2c,2d,2h,2s,6d,7h,8s,9c,10d,jc')
        all_melds = set(tuple(x) for x in score.find_all_melds(hand))
        self.assertEqual(5, len(all_melds))
        self.assertTrue(tuple(Card.from_str_list('2c,2d,2h')) in all_melds)
        self.assertTrue(tuple(Card.from_str_list('2c,2d,2h,2s')) in all_melds)

    def test_find_melds_one_run_of_three(self):
        hand = Card.from_str_list('2c,3c,4c,5d,6d,7h,8s,9c,10d,jc')
        self.assertEqual([Card.from_str_list('2c,3c,4c')], score.find_all_melds(hand))

    def test_find_melds_two_runs_of_three(self):
        hand = Card.from_str_list('2c,3c,4c,5d,6d,7d,8s,9c,10d,jc')
        self.assertEqual([Card.from_str_list('2c,3c,4c'), Card.from_str_list('5d,6d,7d')], score.find_all_melds(hand))

    def test_find_melds_one_run_of_four(self):
        hand = Card.from_str_list('2c,3c,4c,5c,6d,7h,8s,9c,10d,jc')
        all_melds = set(tuple(x) for x in score.find_all_melds(hand))
        self.assertEqual(3, len(all_melds))
        self.assertTrue(tuple(Card.from_str_list('2c,3c,4c')) in all_melds)
        self.assertTrue(tuple(Card.from_str_list('3c,4c,5c')) in all_melds)
        self.assertTrue(tuple(Card.from_str_list('2c,3c,4c,5c')) in all_melds)

    def test_find_melds_run_and_four_of_a_kind(self):
        hand = Card.from_str_list('2c,3c,4c,5c,6d,7h,8c,8s,8d,8h')
        all_melds = set(tuple(x) for x in score.find_all_melds(hand))
        self.assertEqual(8, len(all_melds))
        self.assertTrue(tuple(Card.from_str_list('2c,3c,4c')) in all_melds)
        self.assertTrue(tuple(Card.from_str_list('3c,4c,5c')) in all_melds)
        self.assertTrue(tuple(Card.from_str_list('2c,3c,4c,5c')) in all_melds)
        self.assertTrue(tuple(Card.from_str_list('8c,8s,8d')) in all_melds)
        self.assertTrue(tuple(Card.from_str_list('8c,8s,8d,8h')) in all_melds)

    def test_find_melds_run_and_three_of_a_kind(self):
        hand = Card.from_str_list('2c,3c,4c,4d,4h,7h,8c,9s,10d,jh')
        all_melds = set(tuple(x) for x in score.find_all_melds(hand))
        self.assertEqual(2, len(all_melds))
        self.assertTrue(tuple(Card.from_str_list('2c,3c,4c')) in all_melds)
        self.assertTrue(tuple(Card.from_str_list('4c,4d,4h')) in all_melds)

    def test_find_melds_run_and_four_of_a_kind1(self):
        hand = Card.from_str_list('2c,3c,4c,4d,4h,4s,8c,9s,10d,jh')
        all_melds = set(tuple(x) for x in score.find_all_melds(hand))
        self.assertEqual(6, len(all_melds))
        self.assertTrue(tuple(Card.from_str_list('2c,3c,4c')) in all_melds)
        self.assertTrue(tuple(Card.from_str_list('4c,4d,4h,4s')) in all_melds)

    def test_incorrect_hand_length(self):
        with self.assertRaises(ValueError):
            score.score_hand(Card.from_str_list('1c,2d,3h,4s,5c,6d,7h,8s'))

    def test_no_sequences(self):
        hand = Card.from_str_list('1c,2d,3h,4s,5c,6d,7h,8s,9c,10d')
        all_card_values = sum(x.value for x in hand)
        results = score.score_hand(hand)
        self.assertEqual([], results[0])
        self.assertEqual(hand, results[1])
        self.assertEqual(all_card_values, results[2])

    def test_score_hand_run_and_three_of_a_kind_not_overlapping(self):
        hand = Card.from_str_list('2c,3c,4c,5d,5h,5s,8c,9s,10d,jh')
        results = score.score_hand(hand)
        self.assertEqual(3, len(results))
        best_melds = results[0][0]
        deadwood = results[0][1]
        deadwood_count = results[0][2]
        self.assertEqual(2, len(best_melds))
        self.assertTrue(set(Card.from_str_list('2c,3c,4c')) in best_melds)
        self.assertTrue(set(Card.from_str_list('5d,5h,5s')) in best_melds)
        self.assertEqual(set(Card.from_str_list('8c,9s,10d,jh')), set(deadwood))
        self.assertEqual(37, deadwood_count)

    def test_score_hand_run_and_three_of_a_kind_overlapping(self):
        hand = Card.from_str_list('2c,3c,4c,4d,4h,7h,8c,9s,10d,jh')
        results = score.score_hand(hand)
        self.assertEqual(2, len(results))
        self.assertEqual(49, results[0][2])  # deadwood for the 3 4's meld
        self.assertEqual(52, results[1][2])  # deadwood for the run meld

    def test_score_hand_run_and_four_of_a_kind_not_overlapping(self):
        hand = Card.from_str_list('2c,3c,4c,6c,6d,6h,6s,8c,9s,10d,jh')
        results = score.score_hand(hand)
        best_melds = results[0][0]
        deadwood = results[0][1]
        deadwood_count = results[0][2]
        self.assertEqual(2, len(best_melds))
        self.assertTrue(set(Card.from_str_list('2c,3c,4c')) in best_melds)
        self.assertTrue(set(Card.from_str_list('6c,6d,6h,6s')) in best_melds)
        self.assertEqual(set(Card.from_str_list('8c,9s,10d,jh')), set(deadwood))
        self.assertEqual(37, deadwood_count)

    def test_score_hand_run_and_four_of_a_kind_overlapping(self):
        hand = Card.from_str_list('2c,3c,4c,4d,4h,4s,8c,9s,10d,jh')
        results = score.score_hand(hand)
        self.assertEqual(37, results[0][2])   # deadwood for 3x4's and a run
        self.assertEqual(42, results[1][2])   # deadwood for the 4 4's meld
        self.assertEqual(49, results[-1][2])  # worst hand is the run of 3 on it's own





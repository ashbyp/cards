from cards.holdem.score import eval_desc, eval_hand, best_five_cards, winning_hand
from cards.base.card import Card, hands_equal
from unittest import TestCase


class TestScores(TestCase):

    def setUp(self):
        self.straight_flush = Card.from_str_list("10d jd qd kd ad", sep=' ')
        self.four_of_a_kind = Card.from_str_list("10d 10s 10c 10h ad", sep=' ')
        self.full_house = Card.from_str_list("10d 10s 10s kd ks", sep=' ')
        self.flush = Card.from_str_list("8d jd qd kd ad", sep=' ')
        self.straight = Card.from_str_list("10s jd qd kd ad", sep=' ')
        self.three_of_a_kind = Card.from_str_list("10d 10s 10c kd ad", sep=' ')
        self.two_pair = Card.from_str_list("10d 10s qd qs ad", sep=' ')
        self.one_pair = Card.from_str_list("10d 10s qd kd ad", sep=' ')
        self.high_card = Card.from_str_list("8s jd qd kd ad", sep=' ')

    def test_hands_are_recognised(self):
        self.assertEqual(eval_desc(eval_hand(self.straight_flush)), "Straight Flush")
        self.assertEqual(eval_desc(eval_hand(self.four_of_a_kind)), "Four of a Kind")
        self.assertEqual(eval_desc(eval_hand(self.full_house)), "Full House")
        self.assertEqual(eval_desc(eval_hand(self.flush)), "Flush")
        self.assertEqual(eval_desc(eval_hand(self.straight)), "Straight")
        self.assertEqual(eval_desc(eval_hand(self.three_of_a_kind)), "Three of a Kind")
        self.assertEqual(eval_desc(eval_hand(self.two_pair)), "Two pair")
        self.assertEqual(eval_desc(eval_hand(self.one_pair)), "One pair")
        self.assertEqual(eval_desc(eval_hand(self.high_card)), "High card")

    def test_verbose_descriptions(self):
        self.assertEqual(eval_desc(eval_hand(self.straight_flush), verbose=True), "Straight Flush (Ace high)")
        self.assertEqual(eval_desc(eval_hand(self.four_of_a_kind), verbose=True), "Four of a Kind (10's)")
        self.assertEqual(eval_desc(eval_hand(self.full_house), verbose=True), "Full House (10's over King's)")
        self.assertEqual(eval_desc(eval_hand(self.flush), verbose=True), "Flush (Ace high)")
        self.assertEqual(eval_desc(eval_hand(self.straight), verbose=True), "Straight (Ace high)")
        self.assertEqual(eval_desc(eval_hand(self.three_of_a_kind), verbose=True), "Three of a Kind (10's)")
        self.assertEqual(eval_desc(eval_hand(self.two_pair), verbose=True), "Two pair (Queen's and 10's)")
        self.assertEqual(eval_desc(eval_hand(self.one_pair), verbose=True), "One pair (10's)")
        self.assertEqual(eval_desc(eval_hand(self.high_card), verbose=True), "High card (Ace)")

    def test_return_values(self):
        self.assertEqual(eval_hand(self.straight_flush), (8, 14))
        self.assertEqual(eval_hand(self.four_of_a_kind), (7, 10, [14, 10, 10, 10, 10]))
        self.assertEqual(eval_hand(self.full_house), (6, [10], [13], [13, 13, 10, 10, 10]))
        self.assertEqual(eval_hand(self.flush), (5, [14, 13, 12, 11, 8]))
        self.assertEqual(eval_hand(self.straight), (4, 14))
        self.assertEqual(eval_hand(self.three_of_a_kind), (3, [10], [], [14, 13, 10, 10, 10]))
        self.assertEqual(eval_hand(self.two_pair), (2, [12, 10], [14, 12, 12, 10, 10]))
        self.assertEqual(eval_hand(self.one_pair), (1, [10], [14, 13, 12, 10, 10]))
        self.assertEqual(eval_hand(self.high_card), (0, [], [14, 13, 12, 11, 8]))

    def test_rankings(self):
        self.assertTrue(
            eval_hand(self.straight_flush) >
            eval_hand(self.four_of_a_kind) >
            eval_hand(self.full_house) >
            eval_hand(self.flush) >
            eval_hand(self.straight) >
            eval_hand(self.three_of_a_kind) >
            eval_hand(self.two_pair) >
            eval_hand(self.one_pair) >
            eval_hand(self.high_card)
        )

    def test_equal_hands(self):
        straight1 = Card.from_str_list("10s jd qd kd ad", sep=' ')
        straight2 = Card.from_str_list("10c js qs ks as", sep=' ')
        self.assertEqual(eval_hand(straight1), eval_hand(straight2))

    def test_straight_tie_breaker(self):
        straight1 = Card.from_str_list("9s 10d jd qd kd", sep=' ')
        straight2 = Card.from_str_list("10c js qs ks as", sep=' ')

        self.assertEqual(eval_desc(eval_hand(straight1)), "Straight")
        self.assertEqual(eval_desc(eval_hand(straight2)), "Straight")

        self.assertNotEqual(eval_hand(straight1), eval_hand(straight2))
        self.assertGreater(straight2, straight1)

    def test_pair_tie_breaker(self):
        pair1 = Card.from_str_list("9s 9d jd qd kd", sep=' ')
        pair2 = Card.from_str_list("10c 10s qs ks as", sep=' ')

        self.assertEqual(eval_desc(eval_hand(pair1)), "One pair")
        self.assertEqual(eval_desc(eval_hand(pair2)), "One pair")

        self.assertNotEqual(eval_hand(pair1), eval_hand(pair2))
        self.assertGreater(pair2, pair1)

    def test_ace_handling(self):
        ace_low = Card.from_str_list("1s 2d 3d 4d 5d", sep=' ')
        ace_high = Card.from_str_list("10c js qs ks as", sep=' ')

        self.assertEqual(eval_desc(eval_hand(ace_low)), "Straight")
        self.assertEqual(eval_desc(eval_hand(ace_high)), "Straight")

        self.assertNotEqual(eval_hand(ace_low), eval_hand(ace_high))
        self.assertGreater(eval_hand(ace_high), eval_hand(ace_low))

    def test_input_conditions(self):
        with self.assertRaises(ValueError):
            eval_hand(Card.from_str_list("1s 2d 5d", sep=' '))

    def test_some_straights(self):
        self.assertTrue(
            eval_hand(Card.from_str_list("10s js qs ks as", sep=' ')) >
            eval_hand(Card.from_str_list("9s 10s js qs ks", sep=' ')) >
            eval_hand(Card.from_str_list("As 2s 3s 4s 5s", sep=' ')) >
            eval_hand(Card.from_str_list("10d js qs ks as", sep=' ')) >
            eval_hand(Card.from_str_list("9d 10s js qs ks", sep=' ')) >
            eval_hand(Card.from_str_list("Ad 2s 3s 4s 5s", sep=' '))
        )

    def test_best_five_cards(self):
        with self.assertRaises(ValueError):
            best_five_cards(Card.from_str_list("10d 9s 10c kd", sep=' '))

        hand = sorted(Card.from_str_list("10d 9s 10c kd ad", sep=' '))
        self.assertTrue(hands_equal(best_five_cards(hand)[0], hand))

        hand = Card.from_str_list("10d 3h 10c kd ad 3s 8s 4s qs", sep=' ')
        self.assertTrue(hands_equal(best_five_cards(hand)[0], Card.from_str_list("3h,3s,10d,10c,ad")))

        hand = Card.from_str_list("10d 9s 10c kd ad 3s 8s jd qs", sep=' ')
        self.assertTrue(hands_equal(best_five_cards(hand)[0], Card.from_str_list("10d,jd,qs,kd,ad")))

        hand = Card.from_str_list("10d 10s 10c kd ad 3s 8s jd qs 3c", sep=' ')
        self.assertTrue(hands_equal(best_five_cards(hand)[0], Card.from_str_list("10d,10s,10c,3s,3c")))

        hand = Card.from_str_list("10d 9s 10c kd ad 3s 8s jd qs qd", sep=' ')
        self.assertTrue(hands_equal(best_five_cards(hand)[0], Card.from_str_list("10d,jd,qd,kd,ad")))

    def test_winning_hand_base_cases(self):
        board = []
        hands = []
        with self.assertRaises(ValueError):
            winning_hand(board, hands)

        board = Card.from_str_list("10d,9s,10c,kd,ad")
        hands = []
        with self.assertRaises(ValueError):
            winning_hand(board, hands)

        hands = [Card.from_str_list('Ac,As')]
        winning_hands, winning_scores = winning_hand(board, hands)
        self.assertTrue(len(winning_hands) == 1)
        self.assertTrue(len(winning_scores) == 1)
        self.assertIn(hands[0], winning_hands)
        self.assertEqual(eval_desc(winning_scores[0], verbose=True), "Full House (Ace's over 10's)")

    def test_winning_hand(self):
        board = Card.from_str_list("10d,9s,10c,kd,ad")
        hands = [Card.from_str_list('Ac,As'), Card.from_str_list('2c,As')]
        winning_hands, winning_scores = winning_hand(board, hands)
        self.assertTrue(len(winning_hands) == 1)
        self.assertTrue(len(winning_scores) == 1)
        self.assertIn(hands[0], winning_hands)

        hands = [Card.from_str_list('Ac,As'), Card.from_str_list('2c,As'), Card.from_str_list('Th,Ts')]
        winning_hands, winning_scores = winning_hand(board, hands)
        self.assertTrue(len(winning_hands) == 1)
        self.assertTrue(len(winning_scores) == 1)
        self.assertIn(hands[2], winning_hands)

        board = Card.from_str_list("8d,9s,10c,jd,ad")
        hands = [Card.from_str_list('Qc, 3s'), Card.from_str_list('Qd,2s')]
        winning_hands, winning_scores = winning_hand(board, hands)
        self.assertTrue(len(winning_hands) == 2)
        self.assertTrue(len(winning_scores) == 2)
        self.assertIn(hands[0], winning_hands)
        self.assertIn(hands[1], winning_hands)



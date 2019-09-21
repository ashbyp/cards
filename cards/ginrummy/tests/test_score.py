from unittest import TestCase
from cards.ginrummy import score
from cards.base.card import Card


class TestScore(TestCase):

    def test_incorrect_hand_length(self):
        with self.assertRaises(ValueError):
            score.score_hand(Card.from_str_list('1c,2d,3h,4s,5c,6d,7h,8s'))

    def test_no_sequences(self):
        hand = Card.from_str_list('1c,2d,3h,4s,5c,6d,7h,8s,9c,10d')
        all_card_values = sum(x.value for x in hand)
        sequences, deadwood_count = score.score_hand(hand)
        self.assertFalse(sequences)
        self.assertEqual(all_card_values, deadwood_count)




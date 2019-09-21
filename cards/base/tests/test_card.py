import random
import timeit
from unittest import TestCase
from cards.base.card import Card, standard_deck, split_suits, split_ranks, pairs, three_of_a_kind, four_of_a_kind


class TestCard(TestCase):

    def setUp(self):
        self.ace_of_diamonds = Card(1, 'D')
        self.ten_of_spades = Card(10, 'S')
        self.five_of_clubs = Card(5, 'C')
        self.jack_of_hearts = Card(11, 'H')

    def test_card_constructor_throws_appropriate_exceptions(self):
        with self.assertRaises(ValueError):
            Card('15', 'S')
        with self.assertRaises(ValueError):
            Card('xx', 'S')
        with self.assertRaises(ValueError):
            Card('10', 'NotExist')
        with self.assertRaises(ValueError):
            Card('0', 'S')

    def test_cards_from_str_list(self):
        cards = Card.from_str_list('AD,1D,10S')
        self.assertEqual(cards[0], self.ace_of_diamonds)
        self.assertEqual(cards[1], self.ace_of_diamonds)
        self.assertEqual(cards[2], self.ten_of_spades)

        Card.from_str_list('AD, 1D, 10S')

        with self.assertRaises(ValueError):
            Card.from_str_list('AD,1x,10S')

    def test_from_str(self):
        self.assertEqual(Card.from_str('AD'), self.ace_of_diamonds)
        self.assertEqual(Card.from_str('1D'), self.ace_of_diamonds)
        self.assertEqual(Card.from_str('ad'), self.ace_of_diamonds)
        self.assertEqual(Card.from_str('1d'), self.ace_of_diamonds)

        self.assertEqual(Card.from_str('10S'), self.ten_of_spades)
        self.assertEqual(Card.from_str('10s'), self.ten_of_spades)

        self.assertEqual(Card.from_str('5C'), self.five_of_clubs)
        self.assertEqual(Card.from_str('5c'), self.five_of_clubs)

        self.assertEqual(Card.from_str('JH'), self.jack_of_hearts)
        self.assertEqual(Card.from_str('Jh'), self.jack_of_hearts)
        self.assertEqual(Card.from_str('11H'), self.jack_of_hearts)
        self.assertEqual(Card.from_str('11h'), self.jack_of_hearts)

    def test_set_equality(self):
        c1 = Card.from_str('JH')
        c2 = Card.from_str('JH')
        self.assertEqual(c1, c2)
        self.assertEqual({c1}, {c2})

    def test_sort(self):
        cards = standard_deck()
        random.shuffle(cards)
        cards = sorted(cards)
        self.assertEqual(Card.from_str_list('AC,AD,AH,AS,2C,2D,2H,2S'), cards[0:8])

    def test_card_diff_speed(self):
        deck = set(standard_deck())
        hand = set(Card.from_str_list('2d,3c,4s,5h'))

        x1 = set([x for x in deck if x not in hand])
        x2 = set(deck).difference(hand)

        self.assertEqual(x1, x2)

        start_time = timeit.default_timer()
        for _ in range(1000):
            [x for x in deck if x not in hand]
        list_time_taken = timeit.default_timer() - start_time

        start_time = timeit.default_timer()
        for _ in range(1000):
            deck.difference(hand)
        set_time_taken = timeit.default_timer() - start_time

        print(f'List {list_time_taken} vs Set {set_time_taken}')
        self.assertTrue(set_time_taken < list_time_taken)

    def test_split_suits(self):
        cards = Card.from_str_list('2d,3c,5h,qh')
        suits = split_suits(cards)
        self.assertEqual(4, len(suits))
        self.assertDictEqual(
            suits,
            {'D': [Card.from_str('2d')], 'C': [Card.from_str('3c')], 'H': Card.from_str_list('5h,qh'), 'S': []})

    def test_split_ranks(self):
        cards = Card.from_str_list('2d,3c,5h,5s')
        ranks = split_ranks(cards)
        self.assertEqual(3, len(ranks))
        self.assertDictEqual(
            ranks,
            {2: [Card.from_str('2d')], 3: [Card.from_str('3c')], 5: Card.from_str_list('5h,5s')})

    def test_sets(self):
        cards = Card.from_str_list('AC,AD,AH,AS,2C,2D,2H,3C,3H')
        self.assertEqual(10, len(pairs(cards)))
        self.assertEqual(5, len(three_of_a_kind(cards)))
        self.assertEqual(1, len(four_of_a_kind(cards)))




from unittest import TestCase
from cards.base.utils import all_subsets, remove_subsets, sets_to_sorted_lists
from cards.base.card import Card


class TestCard(TestCase):

    def test_all_subsets_basic(self):
        data = [1, 2, 3]
        subsets = list(all_subsets(data))
        self.assertEqual(8, len(subsets))
        self.assertTrue(() in subsets)
        self.assertTrue((1,) in subsets)
        self.assertTrue((2,) in subsets)
        self.assertTrue((3,) in subsets)
        self.assertTrue((1, 2) in subsets)
        self.assertTrue((1, 3) in subsets)
        self.assertTrue((2, 3) in subsets)
        self.assertTrue((1, 2, 3) in subsets)

    def test_all_subsets_with_lists(self):
        data = [[1, 2, 3], [5, 6, 7]]
        subsets = list(all_subsets(data))
        self.assertEqual(4, len(subsets))
        self.assertTrue(() in subsets)
        self.assertTrue(([1, 2, 3],) in subsets)
        self.assertTrue(([5, 6, 7],) in subsets)
        self.assertTrue(([1, 2, 3], [5, 6, 7]) in subsets)

    def test_all_subsets_basic_cards(self):
        data = [Card.from_str('2c'), Card.from_str('2d'), Card.from_str('2h')]
        subsets = list(all_subsets(data))
        self.assertEqual(8, len(subsets))
        self.assertTrue(() in subsets)
        self.assertTrue((Card.from_str('2c'),) in subsets)
        self.assertTrue((Card.from_str('2d'),) in subsets)
        self.assertTrue((Card.from_str('2h'),) in subsets)
        self.assertTrue((Card.from_str('2c'), Card.from_str('2d')) in subsets)
        self.assertTrue((Card.from_str('2c'), Card.from_str('2h')) in subsets)
        self.assertTrue((Card.from_str('2d'), Card.from_str('2h')) in subsets)
        self.assertTrue((Card.from_str('2c'), Card.from_str('2d'), Card.from_str('2h')) in subsets)

    def test_all_subsets_with_list_of_cards(self):
        data = [Card.from_str_list('2c, 2d, 2s'), Card.from_str_list('3c, 3d, 3s')]
        subsets = list(all_subsets(data))
        self.assertEqual(4, len(subsets))
        self.assertTrue(() in subsets)
        self.assertTrue((Card.from_str_list('2c, 2d, 2s'),) in subsets)
        self.assertTrue((Card.from_str_list('3c, 3d, 3s'),) in subsets)
        self.assertTrue((Card.from_str_list('2c, 2d, 2s'), Card.from_str_list('3c, 3d, 3s')) in subsets)

    def test_remove_subsets(self):
        sets = [set([1, 2, 3]), set([1, 2, 3, 4])]
        removed = remove_subsets(sets)
        self.assertEqual(1, len(removed))
        self.assertEqual(set([1, 2, 3, 4]), removed[0])

    def test_remove_subsets_cards(self):
        sets = [set(Card.from_str_list('2c, 3c, 4c')), set(Card.from_str_list('2c, 3c, 4c, 5c'))]
        removed = remove_subsets(sets)
        self.assertEqual(1, len(removed))
        self.assertEqual(set(Card.from_str_list('2c, 3c, 4c, 5c')), removed[0])

    def test_sets_to_sorted_list(self):
        sets = [set([3, 2, 1]), set([4, 3, 2, 1])]
        lists = sets_to_sorted_lists(sets)
        self.assertEqual([[1, 2, 3], [1, 2, 3, 4]], lists)

    def test_sets_to_sorted_list_cards(self):
        sets = [set(Card.from_str_list('4c, 3c, 2c')), set(Card.from_str_list('5c, 4c, 3c, 2c'))]
        lists = sets_to_sorted_lists(sets)
        self.assertEqual([Card.from_str_list('2c, 3c, 4c'), Card.from_str_list('2c, 3c, 4c, 5c')], lists)


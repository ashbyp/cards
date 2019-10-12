from unittest import TestCase
from cards.base.utils import all_subsets


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
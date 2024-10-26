import unittest
from main import bubble_sort

class Pr1UnitTest(unittest.TestCase):
    def test_sorted(self):
        self.assertEqual(bubble_sort([3, 2, 4, 1, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        self.assertEqual(bubble_sort([10, 9, 8, 7]), [7, 8, 9, 10])

    def test_already_sorted(self):
        self.assertEqual(bubble_sort([1, 2, 3]), [1, 2, 3])

    def test_identical_elements(self):
        self.assertEqual(bubble_sort([5, 5]), [5, 5])

    def test_single_element(self):
        self.assertEqual(bubble_sort([-1]), [-1])

    def test_empty(self):
        self.assertEqual(bubble_sort([]), [])

    def test_with_string(self):
        with self.assertRaises(ValueError) as context:
            bubble_sort([3, 2, 'four', 1, 5])
        self.assertEqual(str(context.exception), "Элементы списка должны быть числами")

    def test_with_nested_list(self):
        with self.assertRaises(ValueError) as context:
            bubble_sort([[10], 9, 8, 7])
        self.assertEqual(str(context.exception), "Элементы списка должны быть числами")

    def test_with_none_in_list(self):
        with self.assertRaises(ValueError) as context:
            bubble_sort([1, 2, None])
        self.assertEqual(str(context.exception), "Элементы списка должны быть числами")

    def test_with_number(self):
        with self.assertRaises(TypeError) as context:
            bubble_sort(55)
        self.assertEqual(str(context.exception), "Входные данные должны быть списком")

    def test_with_set(self):
        with self.assertRaises(TypeError) as context:
            bubble_sort({-1})
        self.assertEqual(str(context.exception), "Входные данные должны быть списком")

    def test_with_none(self):
        with self.assertRaises(TypeError) as context:
            bubble_sort(None)
        self.assertEqual(str(context.exception), "Входные данные должны быть списком")

if __name__ == "__main__":
    unittest.main()

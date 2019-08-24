from polynom import Polynom, compare_with_epsilon
import unittest


class TestPolynomials(unittest.TestCase):
    def test_add_polynom(self):
        first = Polynom({'xyx': 2, 'z': 0, '': 2.539})
        second = Polynom({'xxy': 5j, 'z': -4, 'abcc': 4})
        third = Polynom({'cabc': -2, 'z': 4, '': -2.539})
        self.assertTrue(compare_with_epsilon(Polynom(
            {'xxy': (2+5j), 'abcc': 2}), first + second + third))
        self.assertTrue(compare_with_epsilon(Polynom(
            {'xxy': (2+5j), '': 2.539, 'z': -4, 'abcc': 4}), first + second))
        self.assertTrue(compare_with_epsilon(Polynom(
            {'xxy': 2, 'abcc': -2, 'z': 4}), first + third))
        self.assertTrue(compare_with_epsilon(Polynom(
            {'xxy': 5j, 'abcc': 2, '': -2.539}), second + third))

    def test_add_other(self):
        polynom_ = Polynom({'xyx': 2, 'z': 0, '': 2.539})
        self.assertTrue(compare_with_epsilon(Polynom(
            {'xyx': 2, 'z': 0, '': (2.539 + 5j)}), polynom_ + 5j))
        self.assertTrue(compare_with_epsilon(Polynom(
            {'xyx': 2, 'z': 0, '': (18.039 + 5j)}), polynom_ + 15.5))
        self.assertTrue(compare_with_epsilon(Polynom(
            {'xyx': 2, 'z': 0, '': (-1.961 + 5j)}), polynom_ + -20))
        with self.assertRaises(TypeError):
            polynom_ + 5 * 'asdfgh'

    def test_sub(self):
        first = Polynom({'ggg': 14.5, 'x': 2.539, '': 77})
        second = Polynom({'ggg': (-1j + 1), 'yz': -4, 'ab': 4, '': -77})
        self.assertTrue(compare_with_epsilon(Polynom(
            {'ggg': (13.5+1j), 'yz': 4, 'ab': -4, '': 154, 'x': 2.539}),
            first - second))
        self.assertTrue(compare_with_epsilon(Polynom(
            {'ggg': 14.5, 'x': 2.539, '': 50.7}), first - +26.3))
        self.assertTrue(compare_with_epsilon(0, second - second))
        self.assertTrue(compare_with_epsilon(0.5, second - Polynom(
            {'ggg': (-1j + 1), 'yz': -4, 'ab': 4}) - -77.5))

    def test_mul(self):
        first = Polynom({'x': 5, 'y': -4})
        second = Polynom({'x': -2, 'y': 6})
        self.assertTrue(compare_with_epsilon(Polynom(
            {'xx': -10, 'xy': 38, 'yy': -24}), first * second))
        self.assertTrue(compare_with_epsilon(
            Polynom({'x': -10, 'y': 8}), -2 * first))
        self.assertTrue(compare_with_epsilon(0, second * 0))

    def test_truediv(self):
        polynom_ = Polynom({'xy': 2, 'z': 0.676})
        self.assertTrue(compare_with_epsilon(
            Polynom({'xy': 1, 'z': 0.338}), polynom_ / 2))
        self.assertTrue(compare_with_epsilon(
            Polynom({'xy': 4, 'z': 1.352}), polynom_ / 0.5))
        with self.assertRaises(ArithmeticError):
            polynom_ / Polynom({'x': 25})
        with self.assertRaises(ZeroDivisionError):
            polynom_ / 0

    def test_pow(self):
        polynom_ = Polynom({'x': 1, '': -2})
        self.assertTrue(compare_with_epsilon(
            Polynom({'xx': 1, 'x': -4, '': 4}), polynom_**2.0))
        with self.assertRaises(ArithmeticError):
            polynom_**(-1)
        with self.assertRaises(TypeError):
            polynom_**0.5

    def test_check_new_polynom(self):
        polynom1 = Polynom({'xz': 2, '': 3.5})
        polynom2 = Polynom({'xz': -2, '': -2.5})
        self.assertTrue(compare_with_epsilon(1, polynom1 + polynom2))

    def test_compare_with_epsilon(self):
        polynom1 = Polynom({'xy': 2, '': 6})
        polynom2 = Polynom({'xy': 2, '': -2.5})
        self.assertTrue(compare_with_epsilon(1, polynom1 - polynom2, 10))

from polynom_parser import Parser
from polynom import Polynom, compare_with_epsilon
import unittest


class TestPolynomialsParsing(unittest.TestCase):
    def test_in2post(self):
        self.assertEqual(['x', '2', '-', 'x', '2', '-', '*'],
                         Parser("(x-2)(x-2)").in2post())
        self.assertEqual(['x', '2', '^', '2', 'x', '3', '^', '*', '+', 'x',
                          '2', '^', '4', 'x', '*', '-', '+', '4', '+'],
                         Parser("x^2 + 2x^3 + x^2 -4x+4".replace(
                             ' ', '')).in2post())
        self.assertEqual(['j'], Parser("j").in2post())
        self.assertEqual(['j', '5', 'x', '*', '+'], Parser("j + 5x".replace(
            ' ', '')).in2post())
        self.assertEqual(['j', '2', '*', 'y', '+'],
                         Parser("(j) * 2 + y".replace(' ', '')).in2post())
        self.assertEqual(['x', 'y', '*', 'x', 'y', 'z', '*', '*', '+'],
                         Parser("xy + xyz".replace(' ', '')).in2post())
        print(Parser("x+y-0z").in2post())
        self.assertEqual(['x', 'y', '0', 'z', '*', '-', '+'],
                         Parser("x+y-0z").in2post())
        self.assertEqual(['x', 'y', '+', '+', 'x', '+'],
                         Parser("(x + y)++(x)".replace(' ', '')).in2post())

    def test_get_polynom(self):
        parser = Parser("xyz + xyz".replace(' ', ''))
        self.assertTrue(compare_with_epsilon(Polynom({'xyz': 2}), parser()))
        parser = Parser("(x-2)(x-2)")
        self.assertTrue(compare_with_epsilon(
            Polynom({'xx': 1, 'x': -4, '': 4}), parser()))
        parser = Parser("(x + y)++(x)".replace(' ', ''))
        self.assertTrue(compare_with_epsilon(
            Polynom({'x': 2, 'y': 1}), parser()))
        parser = Parser("x^2 + 2x^3 + x^2 -4x+4".replace(' ', ''))
        self.assertTrue(compare_with_epsilon(Polynom(
            {'xx': 2, 'xxx': 2, 'x': -4, '': 4}), parser()))
        parser = Parser("j")
        self.assertTrue(compare_with_epsilon(Polynom({'': 1j}), parser()))
        parser = Parser("-2j + 5xu".replace(' ', ''))
        self.assertTrue(compare_with_epsilon(
            Polynom({'': -2j, 'xu': 5}), parser()))
        parser = Parser(" -x^2^3".replace(' ', ''))
        self.assertTrue(compare_with_epsilon(
            Polynom({'xxxxxxxx': -1}), parser()))
        parser = Parser("x/(0x + 1)".replace(' ', ''))
        self.assertTrue(compare_with_epsilon(Polynom({'x': 1}), parser()))
        parser = Parser("jjx")
        self.assertTrue(compare_with_epsilon(Polynom({'x': -1}), parser()))

    def test_syntax_errors(self):
        with self.assertRaises(SyntaxError) as e:
            Parser("((xx+1)").check_brackets_sequence()
            self.assertEqual('There is no closing bracket for '
                             'opening bracket at position 0', e.msg)
        with self.assertRaises(SyntaxError) as e:
            Parser("").in2post()
            self.assertEqual('No such numbers or operands', e.msg)
        with self.assertRaises(SyntaxError) as e:
            Parser("2#x").in2post()
            self.assertEqual('Unrecognized char "#" at position 1', e.msg)
        with self.assertRaises(SyntaxError) as e:
            Parser("2a+aa2a").in2post()
            self.assertEqual('Incorrect representation of expression at '
                             'position 5, the reason is "2"', e.msg)
        with self.assertRaises(SyntaxError) as e:
            Parser("x*/2").is_correct_operations()
            self.assertEqual('Incorrect operands sequence starts at '
                             'position 1 with symbol "*"', e.msg)

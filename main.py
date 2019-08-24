import argparse
import sys
from polynom_parser import Parser
from polynom import compare_with_epsilon


def create_parser():
    parser = argparse.ArgumentParser(
        description='Compare two polynomials, enter strings in double quotes, '
                    'if polynomial starts with "-", '
                    'please insert a space after minus')
    parser.add_argument('first_polynomial', type=str)
    parser.add_argument('second_polynomial', type=str)
    parser.add_argument('-e', '--epsilon', type=float, default=1e-9,
                        help='compares polynomials with given epsilon')
    return parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    first_polynom = None
    second_polynom = None
    try:
        first_polynom = Parser(namespace.first_polynomial.replace(' ', ''))
        first_polynom = first_polynom()
    except SyntaxError as e:
        print(e.msg + ' in first polynomial', file=sys.stderr)
        sys.exit(2)
    except ArithmeticError:
        print('Unable to perform arithmetic operations in first polynomial',
              file=sys.stderr)
        sys.exit(3)
    except TypeError:
        print(
            'Invalid data type in the entered expression in first polynomial',
            file=sys.stderr)
        sys.exit(4)
    try:
        second_polynom = Parser(namespace.second_polynomial.replace(' ', ''))
        second_polynom = second_polynom()
    except SyntaxError as e:
        print(e.msg + ' in second polynomial', file=sys.stderr)
        sys.exit(2)
    except ArithmeticError:
        print('Unable to perform arithmetic operations in second polynomial',
              file=sys.stderr)
        sys.exit(3)
    except TypeError:
        print(
            'Invalid data type in the entered expression in second polynomial',
            file=sys.stderr)
        sys.exit(4)
    if compare_with_epsilon(first_polynom, second_polynom, namespace.epsilon):
        print('Polynomials are equal')
        sys.exit(0)
    else:
        print('Polynomials are not equal')
        sys.exit(1)

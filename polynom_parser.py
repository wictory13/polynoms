import re
import string
from polynom import Polynom

COMPLEX_RE = re.compile(r'\d*\s*\+?\s*\d*j')
FLOAT_RE = re.compile(r'\d+\.?\d*')
NOT_DIGIT = re.compile(r'\D+')
DIGIT = re.compile(r'\d')


class Parser:
    PRIORITY = {
        '(': 0,
        ')': 0,
        '+': 1,
        '-': 2,
        '*': 4,
        '/': 4,
        '^': 5
    }

    def __init__(self, str):
        self.str = str
        self.operations = {
            '+': self.add,
            '-': self.sub,
            '*': self.mul,
            '/': self.div,
            '^': self.pow
        }

    def is_operation(self, chr_):
        return chr_ in self.PRIORITY.keys()

    def is_operand(self, chr_):
        return chr_ in string.ascii_lowercase and chr_ != 'j'

    def is_correct_symbol(self, symbol):
        return self.is_operand(symbol) or symbol.isdigit() or symbol == 'j'

    def is_expression_correct(self, i, chr_):
        if 0 < i < len(self.str) - 1:
            if (chr_ in string.ascii_lowercase and
                    self.str[i + 1].isdigit() and self.str[i - 1].isdigit()):
                raise SyntaxError(
                    'Incorrect representation of expression at '
                    'position {}, the reason is "{}"'.format(str(i), chr_))
            if chr_.isdigit() and self.str[i + 1] in string.ascii_lowercase\
                    and self.str[i - 1] in string.ascii_lowercase:
                raise SyntaxError(
                    'Incorrect representation of expression at '
                    'position {}, the reason is "{}"'.format(str(i), chr_))

    def is_correct_symbols(self, i, chr_):
        if (chr_ not in string.ascii_lowercase and
                not self.is_operation(chr_) and not chr_.isdigit()):
            if chr_ == '.' or chr_ == ',':
                raise SyntaxError(
                    'Incorrect representation of float number, '
                    'the reason is "{}" at position {}'.format(chr_, str(i)))
            raise SyntaxError(
                'Unrecognized char "{}" at position {}'.format(chr_, str(i)))

    def is_empty_string(self):
        for symbol in self.str:
            if symbol in string.ascii_lowercase or symbol.isdigit():
                return False
        return True

    def is_correct_operations(self):
        start = ['++', '--', '+-', '-+', '^', '*', '/']
        for seq in start:
            if self.str.startswith(seq):
                raise SyntaxError(
                    'Incorrect symbol(s) "{}" at the beginning'.format(seq))
        for symbol in self.operations.keys():
            if self.str.endswith(symbol):
                raise SyntaxError(
                    'Incorrect symbol(s) "{}" in the end'.format(symbol))
        for i in range(len(self.str)):
            if 0 < i < len(self.str) - 1:
                if self.str[i] in '+-':
                    if (self.str[i - 1] in '+-') and (self.str[i + 1] in '+-'):
                        raise SyntaxError(
                            'Incorrect operands sequence starts at '
                            'position {} with symbol "{}"'.format(
                                str(i - 1), self.str[i - 1]))
                if self.str[i] in '*/^':
                    if self.str[i - 1] in self.operations.keys():
                        raise SyntaxError(
                            'Incorrect operands sequence starts at '
                            'position {} with symbol "{}"'.format(
                                str(i - 1), self.str[i - 1]))
                    if self.str[i + 1] in self.operations.keys():
                        raise SyntaxError(
                            'Incorrect operands sequence starts at '
                            'position {} with symbol "{}"'.format(
                                str(i), self.str[i]))

    def check_brackets_sequence(self):
        brackets_stack = []
        for i in range(len(self.str)):
            if self.str[i] == '(':
                brackets_stack.append(('(', i))
            if self.str[i] == ')':
                if brackets_stack:
                    brackets_stack.pop()
                else:
                    raise SyntaxError(
                        'There is no opening bracket for closing bracket at '
                        'position {}'.format(str(i)))
        if brackets_stack:
            raise SyntaxError(
                'There is no closing bracket for opening bracket at '
                'position {}'.format(str(brackets_stack[0][1])))

    def in2post(self):
        if self.is_empty_string():
            raise SyntaxError('No such numbers or operands')
        self.check_brackets_sequence()
        self.is_correct_operations()
        prev_coeff = False
        stack = []
        result = []
        i = 0
        while i < len(self.str):
            chr_ = self.str[i]
            self.is_expression_correct(i, chr_)
            self.is_correct_symbols(i, chr_)
            if chr_ == '(':
                if i > 0 and (self.str[i - 1] == ')' or self.is_correct_symbol(
                        self.str[i - 1])):
                    stack.append('*')
                stack.append(chr_)
                i += 1
                prev_coeff = False
                continue
            if chr_ == ')':
                for j in range(len(stack) - 1, -1, -1):
                    if stack[j] == '(':
                        stack.pop()
                        break
                    result.append(stack[j])
                    stack.pop()
                i += 1
                prev_coeff = False
                continue
            if self.is_operation(chr_):
                for j in range(len(stack) - 1, -1, -1):
                    if stack[j] == '(':
                        break
                    if (self.PRIORITY[stack[j]] >= self.PRIORITY[chr_] and
                            chr_ != '^' or
                            self.PRIORITY[stack[j]] > self.PRIORITY[chr_] and
                            chr_ == '^'):
                        result.append(stack[j])
                        stack.pop()
                if chr_ == '-' and i > 0 and self.str[i - 1] == '-':
                    result.pop()
                    stack.append('+')
                else:
                    if chr_ == '-' and self.str[i - 1] == '(':
                        result.append('0')
                    stack.append(chr_)
                i += 1
                prev_coeff = False
                continue
            if self.is_operand(chr_):
                if i > 0 and (self.is_operand(
                        self.str[i - 1]) or self.str[i - 1] == ')'):
                    stack.append('*')
                if prev_coeff:
                    for j in range(len(stack) - 1, -1, -1):
                        if stack[j] == '(':
                            break
                        if self.PRIORITY[stack[j]] >= self.PRIORITY['*']:
                            result.append(stack[j])
                            stack.pop()
                    stack.append('*')
                prev_coeff = False
                result.append(chr_)
            if chr_.isdigit() or chr_ == 'j':
                if i > 0 and self.str[i - 1] == ')':
                    stack.append('*')
                complex_ = re.match(COMPLEX_RE, self.str[i:])
                if complex_ is not None:
                    result.append(''.join(complex_.group()))
                    i += len(complex_.group()) - 1
                else:
                    digit = re.match(FLOAT_RE, self.str[i:]).group()
                    result.append(digit)
                    i += len(digit) - 1
                if i > 0 and self.str[i - 1] == 'j':
                    stack.append('*')
                prev_coeff = True
            i += 1
        for item in stack[::-1]:
            result.append(item)
        return result

    def get_polynom(self, expression):
        operands = []
        polynom = None
        for i in range(len(expression)):
            if (self.is_operand(expression[i]) or 'j' in expression[i]
                    or re.match(FLOAT_RE, expression[i])):
                if (re.search(NOT_DIGIT, expression[i]) and
                        '.' not in expression[i] and 'j' not in expression[i]):
                    polynom = Polynom({expression[i]: 1})
                else:
                    types = [int, float, complex]
                    for type_ in types:
                        try:
                            polynom = Polynom({'': type_(expression[i])})
                        except ValueError:
                            continue
                if polynom:
                    operands.append(polynom)
            if self.is_operation(expression[i]):
                operands[-2:] = [
                    self.operations[expression[i]](*operands[-2:])]
        return operands[-1]

    def add(self, first, second=None):
        if second is None:
            return first
        return first + second

    def sub(self, first, second=None):
        if second is None:
            return -first
        return first - second

    def mul(self, first, second):
        return first * second

    def pow(self, expr, _pow):
        if isinstance(_pow, Polynom):
            if _pow.monoms == {}:
                return expr ** 0
            if (isinstance(_pow.monoms[''], complex) and
                    _pow.monoms[''].imag == 0.0):
                return expr ** _pow.monoms[''].real
        if isinstance(_pow, complex) and _pow.imag == 0.0:
            return expr ** _pow.real
        return expr ** _pow

    def div(self, first, second):
        if isinstance(second, Polynom) and list(second.monoms.keys()) == ['']:
            second = second.monoms['']
        return first / second

    def __call__(self):
        return self.get_polynom(self.in2post())

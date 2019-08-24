from copy import copy


def compare_with_epsilon(first, second, epsilon=1e-9):
    diff = first - second
    if isinstance(diff, Polynom):
        return not diff.monoms
    return abs(diff) < epsilon


class Polynom:
    def __init__(self, polynom_dict):
        self.monoms = {}
        new_polynom_dict = {}
        for var_ in polynom_dict:
            new_key = ''.join(sorted(var_))
            if new_key in new_polynom_dict:
                new_polynom_dict[new_key] += polynom_dict[var_]
            else:
                new_polynom_dict[new_key] = polynom_dict[var_]
        for var_ in new_polynom_dict:
            if new_polynom_dict[var_] == 0:
                continue
            self.monoms[var_] = new_polynom_dict[var_]

    def __add__(self, other):
        if isinstance(other, (int, float, complex)):
            if '' not in self.monoms.keys():
                self.monoms[''] = other
            else:
                self.monoms[''] += other
            return self.check_new_polynom(Polynom(self.monoms))
        if not isinstance(other, Polynom):
            raise TypeError
        new_polynom_dict = copy(self.monoms)
        for var_ in self.monoms.keys():
            for other_var in other.monoms.keys():
                if other_var == var_:
                    new_polynom_dict[var_] += other.monoms[var_]
                if other_var not in new_polynom_dict:
                    new_polynom_dict[other_var] = other.monoms[other_var]
        return self.check_new_polynom(Polynom(new_polynom_dict))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, (int, float, complex, Polynom)):
            return -other + self
        raise TypeError

    def __rsub__(self, other):
        return -self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float, complex)):
            new_polynom_dict = {}
            for var_ in self.monoms.keys():
                new_polynom_dict[var_] = self.monoms[var_] * other
            return Polynom(new_polynom_dict)
        if not isinstance(other, Polynom):
            raise TypeError
        new_polynom_dict = {}
        for var_ in self.monoms.keys():
            for other_var in other.monoms.keys():
                if var_ + other_var not in new_polynom_dict:
                    new_polynom_dict[var_ + other_var] = self.monoms[
                                        var_] * other.monoms[other_var]
                else:
                    new_polynom_dict[var_ + other_var] += self.monoms[
                                        var_] * other.monoms[other_var]
        return self.check_new_polynom(Polynom(new_polynom_dict))

    def __rmul__(self, other):
        return self.__mul__(other)

    def check_new_polynom(self, new_polynom):
        if new_polynom.monoms == {}:
            return 0
        if len(new_polynom.monoms) == 1 and '' in new_polynom.monoms.keys():
            return new_polynom.monoms['']
        return new_polynom

    def __truediv__(self, other):
        if isinstance(other, Polynom):
            raise ArithmeticError
        if isinstance(other, (int, float, complex)):
            new_polynom_dict = {}
            for var_ in self.monoms.keys():
                new_polynom_dict[var_] = self.monoms[var_] / other
            return Polynom(new_polynom_dict)
        raise TypeError

    def __int__(self):
        if list(self.monoms.keys()) == ['']:
            return int(self.monoms[''])
        raise TypeError

    def __float__(self):
        if list(self.monoms.keys()) == ['']:
            return float(self.monoms[''])
        raise TypeError

    def __pow__(self, power):
        if int(power) == float(power):
            power = int(power)
        else:
            raise TypeError
        if power < 0:
            raise ArithmeticError
        if power == 0:
            return 1
        new_polynom = copy(self)
        for i in range(power - 1):
            new_polynom *= self
        return self.check_new_polynom(new_polynom)

    def __neg__(self):
        new_polynom_dict = {}
        for var_ in self.monoms.keys():
            new_polynom_dict[var_] = -1 * self.monoms[var_]
        return Polynom(new_polynom_dict)

    def __pos__(self):
        return self

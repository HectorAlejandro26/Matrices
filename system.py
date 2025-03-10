from fractions import Fraction
from copy import deepcopy
from string import ascii_lowercase

_Matrix = list[list[int | Fraction]]
_List = list[int | Fraction]


def _simplify_type(value: int | float | Fraction) -> int | Fraction:
    if isinstance(value, (float, Fraction)):
        if value.is_integer():
            return int(value)
        else:
            return Fraction(value)
    elif isinstance(value, int):
        return value

    else:
        raise TypeError()


def addition_list(l1: list[int | Fraction], l2: list[int | Fraction]):
    if len(l1) != len(l2):
        raise ValueError("Listas son de diferente tamaño.")

    return [_simplify_type(a + b) for a, b in zip(l1, l2)]


class Linear:
    __Matrix: _Matrix
    __EqualsTo: _List

    def __init__(self, m: _Matrix, s: _List):
        self.Matrix = m
        self.EqualsTo = s

    @property
    def Matrix(self): return self.__Matrix

    @Matrix.setter
    def Matrix(self, value):
        n_rows = len(value)
        if n_rows == 0:
            raise ValueError("El numero de filas no puede ser 0.")

        for ri in range(n_rows):
            n_cols = len(value[ri])
            if n_cols == 0:
                raise ValueError("El numero de columnas no puede ser 0.")

            if n_cols != n_rows:
                raise ValueError(
                    "El numero de columnas y filas es diferente."
                )
            for ci in range(n_cols):
                value[ri][ci] = _simplify_type(value[ri][ci])

        self.__Matrix = value

    @property
    def EqualsTo(self):
        return self.__EqualsTo

    @EqualsTo.setter
    def EqualsTo(self, value):
        if len(value) != self.n_rows:
            raise ValueError()

        value = [_simplify_type(i) for i in value]

        self.__EqualsTo = value

    @property
    def n_rows(self): return len(self.Matrix)

    @property
    def n_cols(self): return len(self.Matrix[0])

    def get_item(self, indexes: tuple[int, int]) -> int | Fraction:
        i, j = indexes
        return self.__Matrix[i][j]

    def set_item(self, indexes: tuple[int, int], value: int | float | Fraction):
        i, j = indexes
        self.__Matrix[i][j] = _simplify_type(value)

    def get_row(self, index: int):
        return self.__Matrix[index], self.__EqualsTo[index]

    def get_col(self, index: int):
        return [r[index] for r in self.Matrix]

    def set_row(self, index: int, value, eq):
        if len(value) == self.n_cols:
            for ci in range(self.n_cols):
                self.set_item((index, ci), value[ci])

            self.__EqualsTo[index] = _simplify_type(eq)
        else:
            raise ValueError()

    def set_col(self, index: int, value):
        if len(value) == self.n_rows:
            for ri in range(self.n_rows):
                self.set_item((ri, index), value[ri])
        else:
            raise ValueError()

    def scale_item(self, indexes: tuple[int, int], scalar: int | float | Fraction) -> int | Fraction:
        item = self.get_item(indexes)
        scalar: int | Fraction = _simplify_type(scalar)

        return _simplify_type(item * scalar)

    def scale_row(self, index: int, scalar: int | float | Fraction) -> tuple[_List, int | Fraction]:
        eq = _simplify_type(
            self.EqualsTo[index] * _simplify_type(scalar))
        return [self.scale_item((index, ic), scalar) for ic in range(self.n_cols)], eq

    def scale_col(self, index: int, scalar: int | float | Fraction) -> _List:
        return [self.scale_item((ir, index), scalar) for ir in range(self.n_rows)]

    def __copy__(self):
        return Linear(deepcopy(self.__Matrix), deepcopy(self.__EqualsTo))

    def __repr__(self):
        out = ""
        for ri in range(self.n_rows):
            out += "│"
            row, eq = self.get_row(ri)
            for ci in range(self.n_cols):
                ritem_str = str(row[ci])
                spaces = " " * (max(len(str(n))
                                for n in self.get_col(ci)) - len(ritem_str))
                out += spaces + ritem_str
                out += ", " if ci < self.n_cols - 1 else ""
            out += "┊"
            eitem_str = str(eq)
            spaces = " " * (max(len(str(n))
                            for n in self.__EqualsTo) - len(eitem_str))

            out += spaces + eitem_str + "│\n"

        return out


class _Linear_Solved(Linear):
    __procedure: str

    def __init__(self, m: _Matrix, s: _List, procedure):
        super().__init__(m, s)
        self.__validate_solved()
        self.__procedure = procedure

    def __validate_solved(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                expected = 1 if i == j else 0
                if self.get_item((i, j)) != expected:
                    raise ValueError(
                        "La matriz no está en forma de identidad.")

    @property
    def Procedure(self): return self.__procedure

    def __repr__(self):
        string_index = ascii_lowercase.find(
            "x") if len(self.EqualsTo) < 4 else 0
        out = ""
        for i in range(len(self.EqualsTo)):
            out += ascii_lowercase[string_index + i]
            out += f" = {self.EqualsTo[i]}\n"

        return out

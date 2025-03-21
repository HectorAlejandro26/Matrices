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


def _addition_list(l1: list[int | Fraction], l2: list[int | Fraction]):
    if len(l1) != len(l2):
        raise ValueError("Listas son de diferente tamaño.")

    return [_simplify_type(a + b) for a, b in zip(l1, l2)]


class Matrix:
    __Matrix: _Matrix

    def __init__(self, m: _Matrix):
        self.Matrix = m

    def to_linear(self, equals_to: _List):
        return Linear(self.Matrix, equals_to)

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
    def det(self):
        if self.n_rows > 3:
            return Matrix._expansion_cofactors(self)
        else:
            return Matrix._sarrus(self)

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
        return self.__Matrix[index]

    def get_col(self, index: int):
        return [r[index] for r in self.Matrix]

    def set_row(self, index: int, value: list[int | Fraction]):
        if len(value) == self.n_cols:
            for ci in range(self.n_cols):
                self.set_item((index, ci), value[ci])

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
        return [self.scale_item((index, ic), scalar) for ic in range(self.n_cols)]

    def scale_col(self, index: int, scalar: int | float | Fraction) -> _List:
        return [self.scale_item((ir, index), scalar) for ir in range(self.n_rows)]

    def divide_matrix(
        self,
        start: tuple[int, int] | None = None,
        end: tuple[int, int] | None = None,
        exclude_row: list[int] | None = None,
        exclude_col: list[int] | None = None
    ):
        si, sj = start if start else (0, 0)
        ei, ej = end if end else (self.n_rows, self.n_cols)

        exclude_row = exclude_row if exclude_row else []
        exclude_col = exclude_col if exclude_col else []

        ei = ei if ei < self.n_rows else self.n_rows - 1
        ej = ej if ej < self.n_cols else self.n_cols - 1

        if si > ei or sj > ej:
            raise ValueError("Indices incorrectos.")

        m = []
        for i in range(si, ei + 1):
            if i in exclude_row:
                continue
            m.append([])  # Agrega una nueva fila vacía
            for j in range(sj, ej + 1):
                if j in exclude_col:
                    continue
                # Agregar a la última fila creada
                m[-1].append(self.get_item((i, j)))

        return Matrix(m)

    @staticmethod
    def _expansion_cofactors(m: Matrix) -> int | Fraction:
        if not isinstance(m, Matrix):
            raise TypeError("El argumento debe ser de tipo Matrix.")

        det = 0
        sign = 1
        for fa in range(m.n_cols):
            factor = m.get_item((0, fa)) * sign
            sign *= -1
            new_m = m.divide_matrix(
                end=(m.n_rows - 1, m.n_cols - 1),
                exclude_row=[0],
                exclude_col=[fa])

            if new_m.n_rows < 4:
                det += factor * Matrix._sarrus(new_m)
            else:
                det += factor * Matrix._expansion_cofactors(new_m)

        return _simplify_type(det)

    @staticmethod
    def _sarrus(m: Matrix) -> int | Fraction:
        if not isinstance(m, Matrix):
            raise TypeError("El argumento debe ser de tipo Matrix.")

        if m.n_rows not in [1, 2, 3]:
            raise ValueError("La matriz debe ser de 3x3 o menor.")

        if m.n_rows == 1:
            return m.get_item((0, 0))

        elif m.n_rows == 2:
            aux1 = m.get_item((0, 0)) * m.get_item((1, 1))
            aux2 = m.get_item((0, 1)) * m.get_item((1, 0))

        else:
            aux1 = sum([
                m.get_item((0, 0)) * m.get_item((1, 1)) * m.get_item((2, 2)),
                m.get_item((0, 1)) * m.get_item((1, 2)) * m.get_item((2, 0)),
                m.get_item((0, 2)) * m.get_item((1, 0)) * m.get_item((2, 1))
            ])
            # Lado derecho
            aux2 = sum([
                m.get_item((0, 2)) * m.get_item((1, 1)) * m.get_item((2, 0)),
                m.get_item((0, 0)) * m.get_item((1, 2)) * m.get_item((2, 1)),
                m.get_item((0, 1)) * m.get_item((1, 0)) * m.get_item((2, 2))
            ])

        return _simplify_type(aux1 - aux2)

    def __copy__(self):
        return Matrix(deepcopy(self.__Matrix))

    def __repr__(self):
        out = ""
        for ri in range(self.n_rows):
            out += "│"
            row = self.get_row(ri)
            for ci in range(self.n_cols):
                ritem_str = str(row[ci])
                spaces = " " * (max(len(str(n))
                                for n in self.get_col(ci)) - len(ritem_str))
                out += spaces + ritem_str
                out += ", " if ci < self.n_cols - 1 else ""

            out += "│\n"

        row_len = len(out.split("\n")[0]) - 2
        aux1 = ("┌" + " " * row_len + "┐\n")
        out = aux1 + out

        aux2 = "└" + " " * row_len + "┘\n"
        out += aux2

        return out


class Linear(Matrix):
    __EqualsTo: _List

    def __init__(self, m: _Matrix, s: _List):
        super().__init__(m)
        self.EqualsTo = s

    @property
    def EqualsTo(self):
        return self.__EqualsTo

    @EqualsTo.setter
    def EqualsTo(self, value):
        if len(value) != self.n_rows:
            raise ValueError()

        value = [_simplify_type(i) for i in value]

        self.__EqualsTo = value

    def get_row(self, index: int):
        return super().get_row(index), self.__EqualsTo[index]

    def set_row(self, index: int, value, eq):
        super().set_row(index, value)
        self.__EqualsTo[index] = _simplify_type(eq)

    def scale_row(self, index: int, scalar: int | float | Fraction) -> tuple[_List, int | Fraction]:
        return super().scale_row(index, scalar), _simplify_type(self.EqualsTo[index] * _simplify_type(scalar))

    def scale_col(self, index: int, scalar: int | float | Fraction) -> _List:
        return [self.scale_item((ir, index), scalar) for ir in range(self.n_rows)]

    def cramer(self):
        m = self.__copy__()
        det = m.det
        procedure = f"|A| = {det}\n\n"
        if det == 0:
            raise ValueError("El determinante es 0.")

        string_index = ascii_lowercase.find(
            "x") if len(self.EqualsTo) < 4 else 0

        results = []
        procedure_end = ""
        for i in range(m.n_cols):
            m2 = m.__copy__()
            m2.set_col(i, m.EqualsTo)
            procedure += f"M_{ascii_lowercase[string_index + i]}:\n{m2}"
            new_det = m2.det
            procedure += f"|M_{ascii_lowercase[string_index + i]}| = {new_det}\n\n"
            results.append(
                _simplify_type(
                    Fraction(new_det, det)
                )
            )

            procedure_end += f"{ascii_lowercase[string_index + i]} = ({new_det})/({det})\n"

        for i in range(m.n_cols):
            m.set_col(i, [0 for _ in range(m.n_cols)])
            m.set_item((i, i), 1)

        return _Linear_Solved(m.Matrix, results, f"{procedure}{procedure_end}")

    def gauss_jordan(self):
        linear = self.__copy__()
        if isinstance(linear, _Linear_Solved):
            return linear
        elif not isinstance(linear, Linear):
            raise TypeError("El argumento debe ser de tipo Linear.")

        step_count = 1
        procedure = ""
        for i in range(linear.n_rows):
            aux = linear.get_item((i, i))

            if aux == 0:
                row = linear.get_row(i)
                if all(x == 0 for x in row[0]) and row[1] != 0:
                    raise ValueError(
                        f"El sistema es inconsistente. Fila {i} es contradictoria.")
                continue

            aux = Fraction(1, aux)

            # Convertir elementos parte de la diagonal a 1
            new_ri, new_ei = linear.scale_row(i, aux)
            linear.set_row(i, new_ri, new_ei)

            # Porcedimiento...
            procedure += f"Paso {step_count}:\n{aux}F_{i+1} -> F_{i+1}\n"
            step_count += 1

            for j in range(linear.n_rows):
                if i != j:  # No modificar la diagonal de 1
                    factor = -linear.get_item((j, i))  # Elemento por hacer 0
                    if factor == 0:  # Para ahorrar pasos
                        continue
                    new_rj, new_ej = linear.scale_row(
                        i, factor)  # (-factor)F_i
                    old_rj, old_ej = linear.get_row(j)  # Fila original

                    # Sumar fila escalada a la fila j
                    new_rj = _addition_list(new_rj, old_rj)
                    new_ej += old_ej

                    # Colocamos el resultado en la matriz
                    linear.set_row(j, new_rj, new_ej)

                    # Porcedimiento...
                    procedure += f"Paso {step_count}:\n{factor}F_{i+1} + F_{j+1} -> F_{j+1}\n"
                    procedure += str(linear) + ('\n' if j != linear.n_rows -
                                                1 and i != linear.n_rows - 1 else "")
                    step_count += 1

        return _Linear_Solved(linear.Matrix, linear.EqualsTo, procedure)

    def __copy__(self):
        return Linear(deepcopy(self.Matrix), deepcopy(self.__EqualsTo))

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
                            for n in self.EqualsTo) - len(eitem_str))

            out += spaces + eitem_str + "│\n"

        row_len = len(out.split("\n")[0]) - 2
        divisor = out.split("\n")[0].index("┊")
        aux1 = ("┌" + " " * row_len + "┐\n")
        aux1 = aux1[:divisor] + "╷" + aux1[divisor + 1:]
        out = aux1 + out

        aux2 = "└" + " " * row_len + "┘\n"
        aux2 = aux2[:divisor] + "╵" + aux2[divisor + 1:]
        out += aux2

        return out


class _Linear_Solved(Linear):
    __procedure: str

    def __init__(self, m: _Matrix, s: _List, procedure: str = ""):
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

    def _procedure_clear(self): self.__procedure = ""

    def __copy__(self):
        return _Linear_Solved(
            deepcopy(self.__Matrix),
            deepcopy(self.__EqualsTo),
            self.__procedure
        )

    def __repr__(self):
        string_index = ascii_lowercase.find(
            "x") if len(self.EqualsTo) < 4 else 0
        out = ""
        for i in range(len(self.EqualsTo)):
            out += ascii_lowercase[string_index + i]
            out += f" = {self.EqualsTo[i]}\n"

        return out

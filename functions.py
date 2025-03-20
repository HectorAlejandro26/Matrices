import re
from sympy import Eq, symbols, linear_eq_to_matrix, Float
from string import ascii_lowercase
from fractions import Fraction
from sympy.core.numbers import Float, Rational, Integer


def format_type(value: Float | Integer):
    if isinstance(value, Float):
        n_rat = Rational(value)
        num, den = n_rat.numerator, n_rat.denominator
        return Fraction(num, den)
    elif isinstance(value, Integer):
        return int(value)
    else:
        raise ValueError(f"Invalid type: \'{type(value)}\'")


def get_linear_system(input_str: str) -> tuple[list[list[int | Fraction]], list[int | Fraction]]:
    if not input_str:
        raise ValueError("No se ingresaron ecuaciones")

    input_str = input_str.lower() \
        .replace(" ", "")\
        .replace("\n", ";")

    vars_str = sorted({c for c in input_str if c in ascii_lowercase})
    vars_sym = symbols(vars_str)

    equations = []
    for eq in input_str.split(";"):
        if not eq:
            continue
        if not "=" in eq:
            eq += "=0"
        if "=" in eq:
            left, right = eq.split("=")
            if not left or not right:
                raise ValueError(f"Ecuación \"{eq}\" inválida")

            left = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", left)
            right = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", right)

            left_eq = eval(left, {v: symbols(v) for v in vars_str})
            right_eq = eval(right, {v: symbols(v) for v in vars_str})

            both = Eq(left_eq, right_eq)
            equations.append(both)

    A, b = linear_eq_to_matrix(equations, vars_sym)

    A_list = [[format_type(num) for num in row] for row in A.tolist()]
    b_list = [format_type(num[0]) for num in b.tolist()]

    if len(A_list) == 0:
        raise ValueError("No se encontraron ecuaciones")
    if len(A_list[0]) == 0:
        raise ValueError("No se encontraron variables")
    if len(A_list) != len(b_list):
        raise ValueError(
            f"El número de ecuaciones ({len(A_list)}) no coincide con el número de resultados ({len(b_list)})")
    if len(vars_sym) != len(A_list[0]):
        raise ValueError(
            f"El número de variables ({len(vars_sym)}) no coincide con el número de ecuaciones ({len(A_list[0])})")

    return A_list, b_list

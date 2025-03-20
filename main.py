from functions import get_linear_system
from colorama import Fore
from system import (
    Matrix,
    Linear,
    _Linear_Solved
)
reset = Fore.RESET
msg = Fore.LIGHTCYAN_EX
option = Fore.RESET
option_def = Fore.WHITE
procedure = Fore.WHITE
input_col = Fore.LIGHTGREEN_EX
input_math_col = Fore.LIGHTRED_EX


def main():
    equations_str = input(f"{msg}Ingrese N ecuaciones separadas por \'{option_def};{msg}\':\n" +
                          f"\t{msg}>> {input_math_col}")
    print(f"{msg}Tus eucaciones son:")
    for i, e in enumerate(equations_str.split(";"), 1):
        print(f"{msg}[{option_def}{i}{msg}]:" +
              f" {input_math_col}{e.replace(" ", "").lower()}")

    try:
        m, s = get_linear_system(equations_str)
    except Exception as e:
        print(f"{Fore.RED}Error al leer las ecuaciones: {e}")
        return 1

    try:
        lin = Linear(m, s)
    except Exception as e:
        print(f"{Fore.RED}Error al crear el sistema: {e}")
        return 1

    o = input(f"{msg}Cramer o Gauss-Jordan? {msg}[{option_def}C{msg}|{option}g{msg}]:\n" +
              f"\t{msg}>> {input_col}").lower().replace(" ", "")

    try:
        lin_solved: _Linear_Solved
        if o in ["c", "cramer", ""]:
            lin_solved = lin.cramer()
        elif o in ["g", "gauss", "gauss-jordan", "gj"]:
            lin_solved = lin.gauss_jordan()
        else:
            print(f"{Fore.RED}{ValueError(f"Opción \"{o}\" invalida")}")
            return 1
    except Exception as e:
        print(f"{Fore.RED}Error al resolver el sistema: {e}")
        return 1

    print(f"{procedure}{lin}")
    print(lin_solved.Procedure)
    print(f"{msg}Soluciones:")
    print(f"{input_math_col}{lin_solved}")

    return 0


if __name__ == "__main__":
    exit_code = main()
    print(end=reset)
    exit(exit_code)

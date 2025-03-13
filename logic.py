from system import (
    Matrix,
    Linear,
    _Linear_Solved,
    _addition_list as addition,
    _simplify_type as simplify
)
from fractions import Fraction


def gauss_jordan(linear_sys: Linear):
    # Copia de la matriz original
    # para evitar modificar la matriz original
    linear = linear_sys.__copy__()

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
                new_rj, new_ej = linear.scale_row(i, factor)  # (-factor)F_i
                old_rj, old_ej = linear.get_row(j)  # Fila original

                # Sumar fila escalada a la fila j
                new_rj = addition(new_rj, old_rj)
                new_ej += old_ej

                # Colocamos el resultado en la matriz
                linear.set_row(j, new_rj, new_ej)

                # Porcedimiento...
                procedure += f"Paso {step_count}:\n{factor}F_{i+1} + F_{j+1} -> F_{j+1}\n"
                procedure += str(linear) + '\n'
                step_count += 1

    return _Linear_Solved(linear.Matrix, linear.EqualsTo, procedure[:-1])

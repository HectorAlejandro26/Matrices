from system import Linear
from logic import gauss_jordan

m, e = [
    [1, 1, 1],
    [3, 2, 1],
    [4, 3, 1]
], [
    60,
    95,
    125
]

m: Linear = Linear(m, e)
m_solved = gauss_jordan(m)


print(f"Inicio:\n{m}")
print(m_solved.Procedure)
print(f"Fin:\n{m_solved}")

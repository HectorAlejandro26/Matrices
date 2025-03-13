from system import Linear, Matrix
from logic import gauss_jordan

m = Matrix([
    [1, 4, 7, 8, 5],
    [2, 3, 6, 9, 1],
    [4, 7, 8, 5, 2],
    [3, 6, 9, 1, 4],
    [7, 8, 5, 2, 3]
])

print(m)

print(f"Det = {m.det}")

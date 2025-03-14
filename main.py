from system import Linear, Matrix
from logic import gauss_jordan

matrix = [
    [4, 13, -4],
    [4, -5, 2],
    [25, 21, -32]
]
eq = [75, 65, 10]

linear = Linear(matrix, eq)

res = linear.cramer()

print(res.Procedure)

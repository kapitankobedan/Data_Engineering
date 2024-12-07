import numpy as np
import json

matrix = np.load("../data/first_task.npy")

matrix_props = {
    'sum': 0,
    'avr': 0,
    'sumMD': 0, # главная диагональ
    'avrMD': 0,
    'sumSD': 0, # побочная диагональ
    'avrSD': 0,
    'max': matrix[0][0],
    'min': matrix[0][0]
}

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        el = matrix[i][j]
        matrix_props['sum'] += el
        if i == j:
            matrix_props['sumMD'] += el
        if j == matrix.shape[1] - i - 1:
            matrix_props['sumSD'] += el
        if matrix_props['max'] < el:
            matrix_props['max'] = el
        if matrix_props['min'] < el:
            matrix_props['min'] = el

size = matrix.size
matrix_props['avr'] = matrix_props['sum'] / size
matrix_props['avrMD'] = matrix_props['sumMD'] / matrix.shape[0]
matrix_props['avrSD'] = matrix_props['sumSD'] / matrix.shape[0]

for key in matrix_props.keys():
    matrix_props[key] = float(matrix_props[key])

with open(r"..\result\result2.1.1.json", "w", encoding="utf-8") as file:
    json.dump(matrix_props, file)
    print('Результат записан в result2.1.1.json')

norm_matrix = matrix / matrix_props['sum']
np.save(r"..\result\result2.1.2.npy", norm_matrix)
print('Результат записан в result2.1.2.json')

print(f"Сумма нормированной матрицы = {np.load(r"..\result\result2.1.2.npy").sum()}")
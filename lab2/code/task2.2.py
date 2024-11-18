import os.path

import numpy as np

matrix = np.load(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\data\first_task.npy")

# print(matrix)
# print(matrix.shape)

x = []
y = []
z = []
a = 500 + 74

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if matrix[i][j] > a:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])
np.savez(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\result\result2.2.1.npz", x=x, y=y, z=z)
np.savez_compressed(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\result\result2.2.2.npz", x=x, y=y, z=z)
print('Метод savez сохранил результат в result.2.2.1.npz\nМетод savez_compressed сохранил результат в result.2.2.2.npz')

first_size = os.path.getsize(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\result\result2.2.1.npz")
second_size = os.path.getsize(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\result\result2.2.2.npz")

print(f"savez = {first_size}\nsavez_compressed = {second_size}\ndiff = {first_size-second_size}")


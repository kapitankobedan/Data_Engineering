# 4, 14, 24, …
# Оставляем положительные значения, корень квадратный из которых больше 50
# Сумма по каждой строке
import math
def read_file():
    with open(r"C:\Users\Данила\PycharmProjects\DE_practice1\lab1\data\third_task.txt", encoding="utf-8") as file:
        lines = file.readlines()
        table = []
        for line in lines:
            words = line.strip().split(" ")
            table.append(words)

        return table

def fill_na(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == 'N/A':
                table[i][j] = (table[i][j-1] + int(table[i][j+1]))/2
            else:
                table[i][j] = int(table[i][j])



def filter_and_sum(table):
    result = []
    for row in table:
        sum = 0
        for num in row:
            num = float(num)
            if num > 2500:
                sum += num
        result.append(sum)
    return result

def write_to_file(column):
    with open(r"C:\Users\Данила\PycharmProjects\DE_practice1\lab1\result\third_task_result.txt", "w", encoding="utf-8") as file:
        for num in column:
            file.write(f"{num}\n")
print('Результат записан в файл third_task_result.txt')

table = read_file()
fill_na(table)
result = filter_and_sum(table)
write_to_file(result)
# Варианты 4, 14, 24, …
# Операция в рамках одной строки: среднее значение только положительных значений.
# Операция для полученного столбца: вывод столбца, а также поиск максимального и минимального значения.
# Формат результата:
# average1
# average2
# average3
# -----------
# averageN
#
# max_val
# min_val


def read_file():
    with open(r"C:\Users\Данила\PycharmProjects\DE_practice1\data\second_task.txt", encoding="utf-8") as file:
        lines = file.readlines()
        table = []
        for line in lines:
            words = line.strip().split(" ")
            table.append(list(map(int, words)))
        return table

def first_operation(table):
    result = []
    for row in table:
        positive_sum = 0
        count = 0
        for num in row:
            if num > 0:
                count += 1
                positive_sum += num
        average_positive = positive_sum / count
        result.append(average_positive)
    return result

def find_max(column):
    curr_max = column[0]
    for num in column:
        if num > curr_max:
            curr_max = num
    maximum = curr_max
    return maximum

def find_min(column):
    curr_min = column[0]
    for num in column:
        if num < curr_min:
            curr_min = num
    minimum = curr_min
    return minimum

def second_operation(column, maximum, minimum):
    with open(r"C:\Users\Данила\PycharmProjects\DE_practice1\result\second_task_result.txt", "w", encoding="utf-8") as file:
        for num in column:
            file.write(f"{num}\n")
        file.write(f"\n{maximum}\n{minimum}")
print('Результат записан в second_task_result.txt')

table = read_file()
column = first_operation(table)
maximum = find_max(column)
minimum = find_min(column)
second_operation(column, maximum, minimum)



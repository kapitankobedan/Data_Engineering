# Вариант 74
# 1. Удалите из таблицы столбец expiration_date
# 2. Найдите среднее арифметическое по столбцу quantity
# 3. Найдите максимум по столбцу price
# 4. Найдите минимум по столбцу price
# 5. Отфильтруйте значения, взяв только те, у которых category Овощи
import csv
def read_csv(path):
    data = []
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({
                'product_id': int(row['product_id']),
                'name': row['name'],
                'price': float(row['price']),
                'quantity': int(row['quantity']),
                'category': row['category'],
                'description': row['description'],
                'production_date': row['production_date'],
                #'expiration_date': row['expiration_date'],
                'rating': float(row['rating']),
                'status': row['status']
            })
    return data
def average(data, column):
    size = len(data)
    current_sum = 0
    for item in data:
        current_sum += item[column]
    result = f"Среднее значение в столбце {column}: {round((current_sum / size), 2)}"
    return result
def maximum(data, column):
    current_max = data[0][column]
    for item in data:
        if item[column] > current_max:
            current_max = item[column]
    result = f"Максимум в столбце {column}: {current_max}"
    return result
def minimum(data, column):
    current_min = data[0][column]
    for item in data:
        if item[column] < current_min:
            current_min = item[column]
    result = f"Минимум в столбце {column}: {current_min}"
    return result
def filter(data, column, value_column):
    filtered_data = []
    for item in data:
        if item[column] == value_column:
            filtered_data.append(item)
    result = filtered_data
    return result
def write_to_files(average, maximum, minimum, filter):
    with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab1\result\result1.4.1.txt", "w", encoding="utf-8") as file:
        file.write(f"{average}\n{maximum}\n{minimum}\n")
    with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab1\result\result1.4.2.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, filter[0].keys())
        writer.writeheader()
        for row in filter:
            writer.writerow(row)
data = read_csv(path=r"C:\Users\Данила\PycharmProjects\DE_labs\lab1\data\fourth_task.txt")
average = average(data, 'quantity')
maximum = maximum(data, 'price')
minimum = minimum(data, 'price')
filter = filter(data, 'category', 'Овощи')
write_to_files(average, maximum, minimum, filter)
print('Среднее, максимум и минимум записаны в файл result1.4.1.txt')
print('Отфильтрованнфе данные записаны в result1.4.2.csv')
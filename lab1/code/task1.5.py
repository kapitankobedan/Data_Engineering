import csv

from bs4 import BeautifulSoup



columns = ["product_id", "name", "price", "quantity", "category", "description", "production_date", "expiration_date", "rating", "status"]

to_float = ['price', 'rating']
to_int = ['product_id', 'quantity']

with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab1\data\fifth_task.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

data = []

for row in soup.find_all("tr"):
    cols = row.find_all("td")
    item = {}

    column_index = 0
    for col in cols:
        val = col.get_text(strip=True)
        curr_column = columns[column_index]
        column_index += 1
        item[curr_column] = val

        if curr_column in to_float:
            item[curr_column] = float(val)
        if curr_column in to_int:
            item[curr_column] = int(val)
    if len(item) > 0:
        data.append(item)

with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab1\result\result1.5.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, data[0].keys())
    writer.writeheader()
    for row in data:
        writer.writerow(row)
print('Результат был записан в файл result1.5.csv')
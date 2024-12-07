from bs4 import BeautifulSoup
import json


def handel_file(path):
    with open(path, "r", encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    products = soup.find_all('div', attrs={'class': 'product-item'})

    items = []

    for product in products:
        item = {}
        item['data-id'] = int(product.a['data-id'])
        item['href'] = product.find_all('a')[1]['href']
        item['img'] = product.find_all('img')[0]['src']
        item['title'] = product.span.get_text().strip()
        item['price'] = float(product.price.get_text().replace('₽', '').replace(' ', '').strip())
        item['bonus'] = int(product.strong.get_text()
                            .replace('+ начислим', '')
                            .replace(' бонусов', '')
                            .strip()
                            )
        properties = product.ul.find_all('li')
        for prop in properties:
            item[prop['type']] = prop.get_text().strip()
        items.append(item)
    return items


all_items = []
for i in range(1, 35):
    all_items.extend(handel_file(fr"C:\Users\Данила\PycharmProjects\DE_labs\lab3\data\2\{i}.html"))  # Используем extend вместо append
sorting_criteria = 'data-id'
sorted_items = sorted(all_items, key=lambda x: x[sorting_criteria], reverse=True)
with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab3\result\result3.2.1.json", 'w', encoding="utf-8") as file:
    json.dump(sorted_items, file, ensure_ascii=False)
    print(f"Данные отсортированы по признаку '{sorting_criteria}' и записаны в result3.2.1.json")

filtering_criteria = 'bonus'
minimum_filtering = 4500
filtered_items = []
for item in all_items:
    if item[filtering_criteria] > minimum_filtering:
        filtered_items.append(item)
with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab3\result\result3.2.2.json", 'w', encoding="utf-8") as file:
    json.dump(filtered_items, file, ensure_ascii=False)
    print(f"Данные, значение '{filtering_criteria}' которых больше {minimum_filtering}, записаны в result3.2.2.json")


interesting_criteria = 'price'
total = 0
cur_min = 100000
cur_max = 0
count = 0
for item in all_items:
    total += item[interesting_criteria]
    count += 1
    if item[interesting_criteria] < cur_min:
        cur_min = item[interesting_criteria]
    if item[interesting_criteria] > cur_max:
        cur_max = item[interesting_criteria]
average = total/count
result = f"Статистческие характеристики по признаку '{interesting_criteria}':\n Сумма = {total}\n Максимум = {cur_max}\n Минимум = {cur_min}\n Среднее = {average}"
with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab3\result\result3.2.3.txt", 'w', encoding="utf-8") as file:
    file.write(result)
    print(f"Статистические характеристики по признаку '{interesting_criteria}' записаны в result3.2.3.txt")

interesting_text_criteria = 'sim'
set_of_labels = []
for item in all_items:
    if interesting_text_criteria in item and item[interesting_text_criteria] not in set_of_labels:
        set_of_labels.append(item[interesting_text_criteria])
label_freq = {label: 0 for label in set_of_labels}
for item in all_items:
    if interesting_text_criteria in item:  # Проверяем наличие ключа перед использованием
        label = item[interesting_text_criteria]
        label_freq[label] += 1
with open(r"..\result\result3.2.4.json", 'w', encoding="utf-8") as file:
    json.dump(label_freq, file, ensure_ascii=False)
    print(f"Количества одинковых меток по признаку '{interesting_text_criteria}' записаны в result3.2.4.json")

from bs4 import BeautifulSoup
import lxml
import json
def handel_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        xml_content = file.read()

        clothings = BeautifulSoup(xml_content, 'xml').find_all('clothing')
        items = []
        for clothing in clothings:
            item = {}
            item['id'] = int(clothing.id.get_text())
            item['name'] = clothing.find_all('name')[0].get_text().strip()
            item['category'] = clothing.category.get_text().strip()
            item['size'] = clothing.size.get_text().strip()
            item['color'] = clothing.color.get_text().strip()
            item['material'] = clothing.material.get_text().strip()
            item['price'] = float(clothing.price.get_text().strip())
            item['rating'] = float(clothing.rating.get_text().strip())
            item['reviews'] = int(clothing.reviews.get_text().strip())
            if clothing.new is not None:
                item['new'] = clothing.new.get_text().strip() == '+'
            if clothing.exclusive is not None:
                item['exclusive'] = clothing.exclusive.get_text().strip() == 'yes'
            if clothing.sporty is not None:
                item['sporty'] = clothing.sporty.get_text().strip() == 'yes'
            items.append(item)
        return items


all_items = []
for i in range(1, 223):
    all_items.extend(handel_file(fr"..\data\4\{i}.xml"))
sorting_criteria = 'price'
sorted_items = sorted(all_items, key=lambda x: x[sorting_criteria])
with open(r"..\result\result3.4.1.json", 'w', encoding="utf-8") as file:
    json.dump(sorted_items, file, ensure_ascii=False)
    print(f"Данные отсортированы по признаку '{sorting_criteria}' и записаны в result3.4.1.json")


filtered_items = [item for item in all_items if 'exclusive' in item and item['exclusive']]
with open(r"..\result\result3.4.2.json", 'w', encoding="utf-8") as file:
    json.dump(filtered_items, file, ensure_ascii=False)
    print(f"Данные, значение 'exclusive' которых равно true, записаны в result3.4.2.json")


interesting_criteria = 'rating'
total = 0
cur_min = 100
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
with open(r"..\result\result3.4.3.txt", 'w', encoding="utf-8") as file:
    file.write(result)
    print(f"Статистические характеристики по признаку '{interesting_criteria}' записаны в result3.4.3.txt")

interesting_text_criteria = 'size'
set_of_labels = []
for item in all_items:
    if interesting_text_criteria in item and item[interesting_text_criteria] not in set_of_labels:
        set_of_labels.append(item[interesting_text_criteria])
label_freq = {label: 0 for label in set_of_labels}
for item in all_items:
    if interesting_text_criteria in item:  # Проверяем наличие ключа перед использованием
        label = item[interesting_text_criteria]
        label_freq[label] += 1
with open(r"..\result\result3.4.4.json", 'w', encoding="utf-8") as file:
    json.dump(label_freq, file, ensure_ascii=False)
    print(f"Количества одинковых меток по признаку '{interesting_text_criteria}' записаны в result3.4.4.json")

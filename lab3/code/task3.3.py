from bs4 import BeautifulSoup
import lxml
import json
def handel_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        xml_content = file.read()

        star = BeautifulSoup(xml_content, 'xml').star
        item = {}
        for el in star:
            if el.name is None:
                continue
            item[el.name] = el.get_text().strip()
        item['radius'] = int(item['radius'])
        return(item)

all_items = []
for i in range(1, 245):
    all_items.append(handel_file(fr"..\data\3\{i}.xml"))  # Используем extend вместо append
sorting_criteria = 'name'
sorted_items = sorted(all_items, key=lambda x: x[sorting_criteria])
with open(r"..\result\result3.3.1.json", 'w', encoding="utf-8") as file:
    json.dump(sorted_items, file, ensure_ascii=False)
    print(f"Данные отсортированы по признаку '{sorting_criteria}' и записаны в result3.3.1.json")

filtering_criteria = 'constellation'
minimum_filtering = 'Телец'
filtered_items = []
for item in all_items:
    if item[filtering_criteria] == minimum_filtering:
        filtered_items.append(item)
with open(r"..\result\result3.3.2.json", 'w', encoding="utf-8") as file:
    json.dump(filtered_items, file, ensure_ascii=False)
    print(f"Данные, значение '{filtering_criteria}' которых равно '{minimum_filtering}', записаны в result3.3.2.json")


interesting_criteria = 'radius'
total = 0
cur_min = 1000000000000000000000000000
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
with open(r"..\result\result3.3.3.txt", 'w', encoding="utf-8") as file:
    file.write(result)
    print(f"Статистические характеристики по признаку '{interesting_criteria}' записаны в result3.3.3.txt")

interesting_text_criteria = 'constellation'
set_of_labels = []
for item in all_items:
    if interesting_text_criteria in item and item[interesting_text_criteria] not in set_of_labels:
        set_of_labels.append(item[interesting_text_criteria])
label_freq = {label: 0 for label in set_of_labels}
for item in all_items:
    if interesting_text_criteria in item:  # Проверяем наличие ключа перед использованием
        label = item[interesting_text_criteria]
        label_freq[label] += 1
with open(r"..\result\result3.3.4.json", 'w', encoding="utf-8") as file:
    json.dump(label_freq, file, ensure_ascii=False)
    print(f"Количества одинковых меток по признаку '{interesting_text_criteria}' записаны в result3.3.4.json")

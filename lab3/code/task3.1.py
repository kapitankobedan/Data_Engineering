from bs4 import BeautifulSoup
import json


def handel_file(path):
    with open(path, "r", encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    product = soup.find_all('div', attrs={'class': 'product-wrapper'})[0]

    item = {}
    item['id'] = product.h1["id"]
    item['availability'] = product.find_all("span")[0].get_text().split('Наличие: ')[1].strip()
    item['name'] = product.find_all("h1")[0].get_text().split(':')[1].strip()
    city_temp = product.p.get_text().split('Цена:')[0].strip()
    item['city'] = city_temp.split(':')[1].strip()
    item['price, rub'] = float(product.p.get_text().split('Цена:')[1].split(' руб')[0].strip())
    item['color'] = product.find_all('span', attrs={'class': 'color'})[0].get_text().split(':')[1].strip()
    item['quantity, pieces'] = int(
        product.find_all('span', attrs={'class': 'quantity'})[0].get_text().split(':')[1].split(' шт')[0].strip())
    item['sizes'] = product.find_all("span")[3].get_text().split('Размеры:')[1].strip()
    item['img'] = product.img['src']
    item['rating'] = float(product.find_all("span")[4].get_text().split('Рейтинг: ')[1].strip())
    item['views'] = int(product.find_all("span")[5].get_text().split('Просмотры: ')[1].strip())
    return item


items = []
for i in range(2, 77):
    items.append(handel_file(fr"C:\Users\Данила\PycharmProjects\DE_labs\lab3\data\1\{i}.html"))
sorting_criteria = 'price, rub'
sorted_items = sorted(items, key=lambda x: x[sorting_criteria], reverse=True)
with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab3\result\result3.1.1.json", 'w', encoding="utf-8") as file:
    json.dump(sorted_items, file, ensure_ascii=False)
    print(f"Данные отсортированы по признаку '{sorting_criteria}' и записаны в result3.1.1.json")

filtering_criteria = 'rating'
minimum_filtering = 4.5
filtered_items = []
for item in items:
    if item[filtering_criteria] > minimum_filtering:
        filtered_items.append(item)
with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab3\result\result3.1.2.json", 'w', encoding="utf-8") as file:
    json.dump(filtered_items, file, ensure_ascii=False)
    print(f"Данные, значение '{filtering_criteria}' которых больше {minimum_filtering}, записаны в result3.1.2.json")


interesting_criteria = 'views'
total = 0
cur_min = 1000000
cur_max = 0
count = 0
for item in items:
    total += item[interesting_criteria]
    count += 1
    if item[interesting_criteria] < cur_min:
        cur_min = item[interesting_criteria]
    if item[interesting_criteria] > cur_max:
        cur_max = item[interesting_criteria]
average = total/count
result = f"Статистические характеристики по признаку '{interesting_criteria}':\n Сумма = {total}\n Максимум = {cur_max}\n Минимум = {cur_min}\n Среднее = {average}"
with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab3\result\result3.1.3.txt", 'w', encoding="utf-8") as file:
    file.write(result)
    print(f"Статистческие характеристики по признаку '{interesting_criteria}' записаны в result3.1.3.txt")

interesting_text_criteria = 'color'
set_of_labels = []
for item in items:
    if item[interesting_text_criteria] not in set_of_labels:
        set_of_labels.append(item[interesting_text_criteria])
label_freq = {label: 0 for label in set_of_labels}
for item in items:
    label = item[interesting_text_criteria]
    label_freq[label] += 1
with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab3\result\result3.1.4.json", 'w', encoding="utf-8") as file:
    json.dump(label_freq, file, ensure_ascii=False)
    print(f"Количества одинковых меток по признаку'{interesting_text_criteria}' записаны в result3.1.4.json")

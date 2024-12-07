import requests
from bs4 import BeautifulSoup
import json
from transliterate import translit

# ПАРСИНГ КАТАЛОГА ТОВАРОВ

url = "https://55.mutmarket.ru/catalog/sale"

# Загружаем HTML страницы
response = requests.get(url)

# Проверяем статус ответа
if response.status_code == 200:
    # Создаем объект BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все элементы с товарами
    products = soup.find_all('div', class_='col-xs-12 col-sm-6 col-md-4 col-xl-3')
    items = []
    for product in products:
        item = {}
        item['name'] = product.find('div', class_='product_name').find('a').get_text().strip()
        item['img'] = product.find('div', class_='image').find('img')['src']
        item['price'] = int(product.find('span', class_='fn-price').get_text().strip().replace(' ', ''))
        item['old_price'] = int(product.find('span', class_='fn-old_price').get_text().strip().replace(' ', ''))
        if item['old_price'] == 0:
            item['old_price'] = None
        else:
            discount = 100 - (item['price'] / item['old_price']) * 100
            item['discount, %'] = round(discount, 2)
        if item['img'] == 'design/carol_2/images/no_image.png':
            item['img'] = None
        items.append(item)

sorting_criteria = 'discount, %'
sorted_items = sorted(items, key=lambda x: x[sorting_criteria])
with open(r"..\result\result3.5.1.json", 'w', encoding="utf-8") as file:
    json.dump(sorted_items, file, ensure_ascii=False)
    print(f"Данные о товарах, взятые из каталога {url} и отсортированные по '{sorting_criteria}', записаны в result3.5.1.json")

filtering_criteria = 'price'
maximum_filtering = 1000
filtered_items = []
for item in items:
    if item[filtering_criteria] < maximum_filtering:
        filtered_items.append(item)
with open(r"..\result\result3.5.2.json", 'w', encoding="utf-8") as file:
    json.dump(filtered_items, file, ensure_ascii=False)
    print(f"Данные из {url}, значение '{filtering_criteria}' которых не превышает {maximum_filtering}, записаны в result3.5.2.json")

interesting_criteria = 'old_price'
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
with open(r"..\result\result3.5.3.txt", 'w', encoding="utf-8") as file:
    file.write(result)
    print(f"Статистческие характеристики для данных из {url} по признаку '{interesting_criteria}' записаны в result3.5.3.txt")


interesting_text_criteria = 'name'
set_of_labels = []
for item in items:
    if item[interesting_text_criteria] not in set_of_labels:
        set_of_labels.append(item[interesting_text_criteria])
label_freq = {label: 0 for label in set_of_labels}
for item in items:
    label = item[interesting_text_criteria]
    label_freq[label] += 1
with open(r"..\result\result3.5.4.json", 'w', encoding="utf-8") as file:
    json.dump(label_freq, file, ensure_ascii=False)
    print(f"Количества одинковых меток по признаку '{interesting_text_criteria}' в каталоге {url} записаны в result3.5.4.json")



# ПАРСИНГ ТОВАРОВ С ОТДЕЛЬНЫХ СТРАНИЦ

base_url = "https://55.mutmarket.ru/catalog/sport-i-otdyh"

# Загружаем HTML страницы
response = requests.get(base_url)

# Проверяем статус ответа
if response.status_code == 200:
    # Создаем объект BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')


# Находим все элементы с товарами
products = soup.find_all('div', class_='col-xs-12 col-sm-6 col-md-4 col-xl-3')
urls = []
for product in products:
    url = product.a['href'].strip()
    urls.append(url)

products_info = []
for url in urls:
    product_info = {}
    product_url = f'https://55.mutmarket.ru/{url}'
    response = requests.get(product_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    product = soup.find('div', class_='col-xs-12 col-lg-9')
    product_info['name'] = product.find('h1', class_='h2').get_text().strip()
    product_info['id'] = product.find('span', class_='fn-sku').get_text().strip()
    product_info['rating'] = product.find('span', class_='rating_value').get_text().strip()
    product_info['rating_value'] = float(product.find('span', class_='rating_value').get_text().strip())
    product_info['rating_count'] = int(product.find('span', class_='rating_count').get_text().strip())
    product_info['in_stock'] = product.find('span', class_='in_stock').get_text().strip() == 'Есть на складе'
    product_info['price'] = int(product.find('span', class_='fn-price').get_text().strip().replace(' ', ''))
    product_info['old_price'] = int(product.find('span', class_='fn-old_price').get_text().strip().replace(' ', ''))
    if product_info['old_price'] == 0:
        product_info['old_price'] = None
    else:
        discount = 100 - (product_info['price'] / product_info['old_price']) * 100
    product_info['img'] = product.img['src']
    product_info['description'] = product.find('div', id='description').get_text().strip()
    product_info['delivery'] = product.find('div', id='delivery').get_text().strip()
    product_info['comments'] = product.find('div', id='comments').get_text().strip()
    products_info.append(product_info)

sorting_criteria = 'price'
sorted_items = sorted(products_info, key=lambda x: x[sorting_criteria])
with open(r"..\result\result3.5.5.json", 'w', encoding="utf-8") as file:
    json.dump(sorted_items, file, ensure_ascii=False)
    print(f"Данные о товарах, взятые со страниц товаров каталога {base_url} и отсортированные по '{sorting_criteria}' записаны в result3.5.5.json")


filtering_criteria = 'in_stock'
maximum_filtering = True
filtered_items = []
for item in products_info:
    if item[filtering_criteria] == maximum_filtering:
        filtered_items.append(item)
with open(r"..\result\result3.5.6.json", 'w', encoding="utf-8") as file:
    json.dump(filtered_items, file, ensure_ascii=False)
    print(f"Данные из {base_url}, значение '{filtering_criteria}' которых является {maximum_filtering}, записаны в result3.5.6.json")

interesting_criteria = 'price'
total = 0
cur_min = 1000000
cur_max = 0
count = 0
for item in products_info:
    total += item[interesting_criteria]
    count += 1
    if item[interesting_criteria] < cur_min:
        cur_min = item[interesting_criteria]
    if item[interesting_criteria] > cur_max:
        cur_max = item[interesting_criteria]
average = total/count
result = f"Статистические характеристики по признаку '{interesting_criteria}':\n Сумма = {total}\n Максимум = {cur_max}\n Минимум = {cur_min}\n Среднее = {average}"
with open(r"..\result\result3.5.7.txt", 'w', encoding="utf-8") as file:
    file.write(result)
    print(f"Статистческие характеристики для данных из {base_url} по признаку '{interesting_criteria}' записаны в result3.5.7.txt")


interesting_text_criteria = 'in_stock'
set_of_labels = []
for item in products_info:
    if item[interesting_text_criteria] not in set_of_labels:
        set_of_labels.append(item[interesting_text_criteria])
label_freq = {label: 0 for label in set_of_labels}
for item in products_info:
    label = item[interesting_text_criteria]
    label_freq[label] += 1
with open(r"..\result\result3.5.8.json", 'w', encoding="utf-8") as file:
    json.dump(label_freq, file, ensure_ascii=False)
    print(f"Количества одинковых меток по признаку '{interesting_text_criteria}' в каталоге {base_url} записаны в result3.5.8.json")

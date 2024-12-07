import json
import msgpack
import os

def read_json(path):
    with open(path,"r", encoding="utf-8") as file:
        return json.load(file)


products = read_json(r"..\data\third_task.json")
products_stat = {}

for product in products:
    name = product['name']
    price = product['price']
    if name not in products_stat:
        products_stat[name] = {
            'name': name,
            'max_price': price,
            'min_price': price,
            'avg_price': price,
            'count': 1,
        }
    else:
        if products_stat[name]['max_price'] < price:
            products_stat[name]['max_price'] = price
        if products_stat[name]['min_price'] > price:
            products_stat[name]['min_price'] = price
        products_stat[name]['avg_price'] += price
        products_stat[name]['count'] += 1

for name in products_stat:
    stat = products_stat[name]
    products_stat[name]['avg_price'] /= stat['count']

to_save = list(products_stat.values())


with open(r"..\result\result2.3.1.json", "w", encoding="utf-8") as file:
    json.dump(to_save, file, ensure_ascii=False)
    print("Результат в формате json записан в result2.3.1.json")

with open(r"..\result\result2.3.2.msgpack", "wb") as file:
    msgpack.dump(to_save, file)
    print("Результат в формате msgpack записан в result2.3.2.msgpack")

first_size = os.path.getsize(r"..\result\result2.3.1.json")
second_size = os.path.getsize(r"..\result\result2.3.2.msgpack")

print(f"json = {first_size}\nmsgpack = {second_size}\ndiff = {first_size-second_size}") 
import pickle
import json

with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\data\fourth_task_products.json", "rb") as file:
    products = pickle.load(file)
    # print(products)
with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\data\fourth_task_updates.json", "r", encoding="utf-8") as file:
    updates = json.load(file)
    # print(updates)

for update in updates:
    product_in_updates = update['name']
    if update['method'] == "sub":
        for product in products:
            product_in_products = product['name']
            if product_in_updates == product_in_products:
                product['price'] -= update['param']
    if update['method'] == "add":
        for product in products:
            product_in_products = product['name']
            if product_in_updates == product_in_products:
                product['price'] += update['param']
    if update['method'] == "percent+":
        for product in products:
            product_in_products = product['name']
            if product_in_updates == product_in_products:
                product['price'] *= 1 + update['param']
    if update['method'] == "percent-":
        for product in products:
            product_in_products = product['name']
            if product_in_updates == product_in_products:
                product['price'] *= 1 - update['param']

# print(products)

with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\result\result2.4.pkl", "wb") as file:
    pickle.dump(products, file)
    print('Результат записан в result2.4.pkl')
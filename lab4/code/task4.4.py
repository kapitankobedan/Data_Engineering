import pickle
import csv
import json
from lab4.code.common import connect_to_db, to_json

def read_pkl(pkl_path, json_path):
    with open(pkl_path, "rb") as pkl_file:
        data = pickle.load(pkl_file)
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

read_pkl('../data/4/_update_data.pkl', '../data/4/_update_data.json')

def create_table2(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE products (
            id integer primary key,
            name text,
            price float,
            quantity integer,
            category text,
            fromCity float,
            isAvailable text,
            views integer,
            version integer default 0)
    """)

def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO products (name, price, quantity, category, fromCity, isAvailable, views)
        VALUES (:name, :price, :quantity, :category, :fromCity, :isAvailable, :views)
    """, items)
    db.commit()

def handle_remove(db, name):
    cursor = db.cursor()
    cursor.execute('DELETE FROM products WHERE name = ?', [name])
    db.commit()

def handle_price_percent(db, name, param):
    cursor = db.cursor()
    cursor.execute('UPDATE products SET price = ROUND(price * (1 + ?), 2), version = version + 1 WHERE name = ?', [param, name])
    db.commit()

def handle_price_abs(db, name, param):
    cursor = db.cursor()
    cursor.execute('UPDATE products SET price = price + ?, version = version + 1 WHERE name = ?', [param, name])
    db.commit()

def handle_quantity_add(db, name, param):
    cursor = db.cursor()
    cursor.execute('UPDATE products SET quantity = quantity + ?, version = version + 1 WHERE name = ?', [param, name])
    db.commit()

def handle_quantity_sub(db, name, param):
    cursor = db.cursor()
    cursor.execute('UPDATE products SET quantity = quantity + ?, version = version + 1 WHERE name = ?', [param, name])
    db.commit()

def handle_available(db, name, param):
    cursor = db.cursor()
    cursor.execute('UPDATE products SET isAvailable = ?, version = version + 1 WHERE name = ?', [param, name])
    db.commit()


def update_data(db, path):
    with open(path, "r", encoding="utf-8") as file:
        upds = json.load(file)
    for upd in upds:
        if upd['method'] == 'remove':
            handle_remove(db, upd['name'])
        elif upd['method'] == 'price_percent':
            handle_price_percent(db, upd['name'], upd['param'])
        elif upd['method'] == 'price_abs':
            handle_price_abs(db, upd['name'], upd['param'])
        elif upd['method'] == 'quantity_add':
            handle_quantity_add(db, upd['name'], upd['param'])
        elif upd['method'] == 'quantity_sub':
            handle_quantity_sub(db, upd['name'], upd['param'])
        elif upd['method'] == 'available':
            handle_available(db, upd['name'], upd['param'])

def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM products
        ORDER BY version DESC
        LIMIT 10;
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT category, SUM(price), MIN(price), MAX(price), AVG(price)
        FROM products
        GROUP BY category;
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT category, SUM(quantity), MIN(quantity), MAX(quantity), AVG(quantity)
        FROM products
        WHERE isAvailable = 1
        GROUP BY category;
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

# Анализ цен для остатков товаров, сгруппированных по городам
def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT fromCity, SUM(price), MIN(price), MAX(price), AVG(price)
        FROM products
        WHERE isAvailable = 1
        GROUP BY fromCity;
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

# STEP 1
db = connect_to_db('../result/third.db')
# create_table2(db)
# STEP 2
# with open(r"../data/4/_product_data.json", "r", encoding="utf-8") as file:
#     items = json.load(file)
#     data = []
#     for item in items:
#         if 'category' not in item:
#             item['category'] = None
#         data.append(item)
# insert_data(db, data)
# STEP 3
# update_data(db, r"../data/4/_update_data.json")
# QUERY 1
to_json('../result/result4.4.1.json', first_query(db))
# QUERY 2
to_json('../result/result4.4.2.json', second_query(db))
# QUERY 3
to_json('../result/result4.4.3.json', third_query(db))
# QUERY 4
to_json('../result/result4.4.4.json', fourth_query(db))
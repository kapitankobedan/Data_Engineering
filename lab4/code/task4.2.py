import msgpack

from lab4.code.common import connect_to_db, to_json

def read_msgpack(path):
    with open(path, "rb") as file:
        data = msgpack.load(file)
        return data

def create_table2(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE another_someDB(
            id integer primary key,
            name text references someDB(name),
            rating float,
            convenience integer,
            security integer,
            functionality integer,
            comment text)
    """)

def insert_data2(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO another_someDB (name, rating, convenience, security, functionality, comment)
        VALUES (:name, :rating, :convenience, :security, :functionality, :comment)
    """, items)
    db.commit()

# Найти средний рейтинг для объектов, у которых просмотры больше 85000
def first_query2(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT s.name, AVG(a.rating) AS average_rating 
        FROM someDB AS s
        JOIN another_someDB AS a 
        ON s.name = a.name
        WHERE s.views > 85000
        GROUP BY s.name;
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

# Средняя безопасность для объектов разной этажности
def second_query2(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT s.floors, AVG(a.security)
        FROM someDB AS s
        JOIN another_someDB AS a ON s.name = a.name
        GROUP BY s.floors;
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

# Самый старый объект со средней функциональностью выше 3
def third_query2(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT s.year, s.name, AVG(a.functionality) AS avg_functionality
        FROM someDB AS s
        JOIN another_someDB AS a ON s.name = a.name
        GROUP BY s.name
        HAVING AVG(a.functionality) > 3
        ORDER BY s.year
        LIMIT 1;
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

# STEP 1
items = read_msgpack(r'..\data\1-2\subitem.msgpack')
# STEP 2
db = connect_to_db('../result/first.db')
# create_table2(db)
# STEP 3
# insert_data2(db, items)
# QUERY 1
to_json('../result/result4.2.1.json', first_query2(db))
# QUERY 2
to_json('../result/result4.2.2.json', second_query2(db))
# QUERY 3
to_json('../result/result4.2.3.json', third_query2(db))
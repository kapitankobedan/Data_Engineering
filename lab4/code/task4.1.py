from lab4.code.common import connect_to_db, to_json


def load_text(filename):
    items = []
    item = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line == '=====':
                if item:
                    items.append(item)
                    item = {}
            else:
                if '::' in line:
                    key = line.split('::')[0]
                    value = line.split('::')[1]
                    if key == 'id' or key == 'zipcode' or key == 'floors' or key == 'year' or key == 'prob_price' or key == 'views':
                        value = int(value)
                    if key == 'parking':
                        if value in [1, 'True']:
                            value = True
                        elif value in [0, 'False']:
                            value = False
                    item[key] = value
        if item:
            items.append(item)

    return items


def create_table1(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE someDB (
            id integer, 
            name text, 
            street text,
            city text,
            zipcode integer,
            floors integer, 
            year integer,
            parking boolean, 
            prob_price integer,
            views integer)
    """)


def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO someDB (id, name, street, city, zipcode, floors, year, parking, prob_price, views)
        VALUES (:id, :name, :street, :city, :zipcode, :floors, :year, :parking, :prob_price, :views)
    """, items)
    db.commit()


def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM someDB
        ORDER BY views
        LIMIT 84
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items


def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT  
            SUM(views),
            MIN(views),
            MAX(views),
            AVG(views)
        FROM someDB
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items[0]


def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT  
            COUNT(*) as count,
            city
        FROM someDB
        GROUP BY city
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM someDB
        WHERE year > 1800
        ORDER BY floors DESC 
        LIMIT 84
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items


# STEP 1
# create_table1(connect_to_db('../result/first.db'))
# STEP 2
# items = load_text('../data/1-2/item.text')
db = connect_to_db('../result/first.db')
# insert_data(db, items)
# QUERY 1
to_json(r"..\result\result4.1.1.json", first_query(db))
# # QUERY 2
to_json(r"..\result\result4.1.2.json", second_query(db))
# # QUERY 3
to_json(r"..\result\result4.1.3.json", third_query(db))
# # QUERY 3
to_json(r"..\result\result4.1.4.json", fourth_query(db))
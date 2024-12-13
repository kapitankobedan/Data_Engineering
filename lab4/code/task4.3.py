import pickle
import csv
import json
from lab4.code.common import connect_to_db, to_json

def read_pkl(path):
    with open(path, "rb") as file:
        data = pickle.load(file)
        for item in data:
            if 'acousticness' in item:
                del item['acousticness']
            if 'popularity' in item:
                del item['popularity']
            if 'duration_ms' in item:
                item['duration_ms'] = int(item['duration_ms'])
            if 'year' in item:
                item['year'] = int(item['year'])
            if 'tempo' in item:
                item['tempo'] = float(item['tempo'])
            if 'energy' in item:
                item['energy'] = float(item['energy'])
        return data

# to_json('data_from_pkl.json', read_pkl('../data/3/_part_2.pkl'))

def read_csv(path):
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Пропускаем первую строку, если это заголовок
        return [
            {
                'artist': row[0],
                'song': row[1],
                'duration_ms': int(row[2]),
                'year': int(row[3]),
                'tempo': float(row[4]),
                'genre': row[5],
                'energy': float(row[6])
            }
            for row in reader if row  # Игнорируем пустые строки
        ]

# to_json('data_from_csv.json', read_csv('../data/3/_part_1.csv'))

def create_table2(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE songs (
            id integer primary key,
            artist text,
            song text,
            duration_ms integer,
            year integer,
            tempo float,
            genre text,
            energy float)
    """)

def insert_data2(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO songs (artist, song, duration_ms, year, tempo, genre, energy)
        VALUES (:artist, :song, :duration_ms, :year, :tempo, :genre, :energy)
    """, items)
    db.commit()

def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM songs
        ORDER BY year DESC
        LIMIT 84;
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT SUM(duration_ms), MIN(duration_ms), MAX(duration_ms), AVG(duration_ms)
        FROM songs
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT artist, COUNT(artist) AS count
        FROM songs
        GROUP BY artist
        ORDER BY count DESC;
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM songs
        WHERE year > 2017
        ORDER BY energy DESC 
        LIMIT 89
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

# STEP 1
part_2 = read_pkl('../data/3/_part_2.pkl')
part_1 = read_csv('../data/3/_part_1.csv')
to_json('../data/3/json_data.json', part_2)
with open(r"../data/3/json_data.json", "r", encoding="utf-8") as file:
    items = json.load(file)
# STEP 2
db = connect_to_db('../result/second.db')
# create_table2(db)
# STEP 3
# insert_data2(db, items)
# # QUERY 1
to_json('../result/result4.3.1.json', first_query(db))
# # QUERY 2
to_json('../result/result4.3.2.json', second_query(db))
# # QUERY 3
to_json('../result/result4.3.3.json', third_query(db))
# # QUERY 3
to_json('../result/result4.3.4.json', fourth_query(db))
import sqlite3
import json

def connect_to_db(filename):
    conn = sqlite3.connect(filename) # если никакой базы данных нет, но все равно используем эту функцию, то будет создан новый файл
    conn.row_factory = sqlite3.Row
    return conn

def to_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Результат в формате json записан в {path}")
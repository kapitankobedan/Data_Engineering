import pymongo
from pymongo import MongoClient
import pickle
import csv
import json

def to_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Результат в формате json записан в {path}")

def connect_db():
    client = MongoClient()
    db = client["basket_players"]
    print(db.stats)
    return db.stats

def read_pkl(path):
    with open(path, "rb") as file:
        data = pickle.load(file)
        if 'Season' in data.columns:
            data['Season'] = data['Season'].str.split('-').str[0].astype(int)
        if 'Salary' in data.columns:
            data['Salary'] = data['Salary'].str.replace('$', '').astype(int)
        items = data.to_dict(orient="records")
        return items

def read_csv(path):
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        return [
            {
                'Season': int(row[0].split('-')[0]),
                'Age': int(row[1]),
                'Tm': row[2],
                'Lg': row[3],
                'Pos': row[4],
                'G': row[5],
                'MP': row[6],
                'PER': float(row[7]),
                'TS': round((float(row[8].replace('.', '')) * 0.1), 2),
                'THPAr': float(row[9].replace('.', '')) * 0.1,
                'FTr': round((float(row[10].replace('.', '')) * 0.1), 2),
                'ORB': float(row[11]),
                'DRB': float(row[12]),
                'TRB': float(row[13]),
                'AST': float(row[14]),
                'STL': float(row[15]),
                'BLK': float(row[16]),
                'TOV': float(row[17]),
                'USG': float(row[18]),
                'OWS': float(row[19]),
                'DWS': float(row[20]),
                'WS': float(row[21]),
                'WS48': round((float(row[22].replace('.', '')) * 0.1), 2),
                'OBPM': float(row[23]),
                'DBPM': float(row[24]),
                'BPM': float(row[25]),
                'VORP': float(row[26]),
                'Player': row[27],
                'RSorPO': row[28]
            }
            for row in reader if row
        ]

# Вывод топ-10 зарплат, отсортированных по убыванию
def query1(collection):
    data = list(collection.find(limit=10).sort("Salary", pymongo.DESCENDING))
    result = []
    for item in data:
        item.pop('_id', None)
        result.append(item)
    return result

# Вывод команд, за которые играл Леброн Джеймс
def query2(collection):
    data = collection.distinct("Team", {"Player": "Lebron James"})
    result = []
    for item in data:
        result.append(item)
    return result

collection = connect_db()
# collection.insert_many(read_pkl('../data/4/salaries.pkl'))
# collection.insert_many(read_csv('../data/4/advanced_stats.csv'))
to_json('../result/result5.4.1.json', query1(collection))
to_json('../result/result5.4.2.json', query2(collection))


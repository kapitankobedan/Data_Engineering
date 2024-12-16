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

# Вывод топ-20 сезонов среди рассматриваемых игроков по рейтингу эффективности
def query2(collection):
    data = list(collection.find(limit=10).sort("PER", pymongo.DESCENDING))
    result = []
    for item in data:
        item.pop('_id', None)
        result.append(item)
    return result

# Вовод топ-15 сезонов Кобе Брайанта по процентам результативных передач
def query3(collection):
    data = list(collection
                .find({'Player': 'Kobe Bryant'}, limit=15)
                .sort("AST", pymongo.DESCENDING))
    result = []
    for item in data:
        item.pop('_id', None)
        result.append(item)
    return result

# Вывод статистики по регулярынм сезонам для Джордана и Брайанта, отсортированной по рейтингу эффективности.
# Для справки: Джордан закончил играть в 2002, а Брайант начал играть в 1996.
# При этом Джордан не играл 1998, 1999, 2000.
def query4(collection):
    data = list(collection
                .find({'Season': {'$gt': 1995, '$lte': 2002}, 'Player': {'$in': ['Michael Jordan', 'Kobe Bryant']}, 'PER': {'$gt': 0}, 'RSorPO': 'Regular Season'})
                .sort("PER", pymongo.DESCENDING))
    result = []
    for item in data:
        item.pop('_id', None)
        result.append(item)
    return result

# Для проверки предыдущего запроса: вывод количества сезонов, которые Джордан и Брайант провели вместе.
def query5(collection):
    return collection.count_documents({
        'Season': {'$gt': 1995, '$lte': 2002},
        'RSorPO': 'Regular Season',
        'PER': {'$gt': 0},
        '$or': [
            {'Player': 'Michael Jordan'},
            {'Player': 'Kobe Bryant'}
        ]
    })

# Статистика по зарплате Джорана за всю его карьеру
def query6(collection):
    q = [
        {
            '$match': {'Player': 'Michael Jordan'}
        },
        {
            '$group': {
                '_id': None,
                'max_salary': {'$max': '$Salary'},
                'min_salary': {'$min': '$Salary'},
                'avg_salary': {'$avg': '$Salary'}
            }
        }
    ]
    data = collection.aggregate(q)
    result = []
    for item in data:
        item.pop('_id', None)
        result.append(item)
    return result

# Количество сезонов в карьере (данные оторваны от реальности) каждого игрока
def query7(collection):
    q = [
        {
            '$match': {'RSorPO': 'Regular Season'}
        },
        {
            '$group': {
                '_id': '$Player',
                'count': {'$sum': 1}
            }
        }
    ]
    data = collection.aggregate(q)
    result = []
    for item in data:
        result.append(item)
    return result

# Статистика по рейтингу эффективности Леброна Джеймса в играх плей-офф за всю его карьеру
def query8(collection):
    q = [
        {
            '$match': {'RSorPO': 'Playoffs'}
        },
        {
            '$match': {'Player': 'Lebron James'}
        },
        {
            '$group': {
                '_id': f'$Player',
                f'max_PER': {'$max': f'$PER'},
                f'min_PER': {'$min': f'$PER'},
                f'avg_PER': {'$avg': f'$PER'}
            }
        }
    ]
    data = collection.aggregate(q)
    result = []
    for item in data:
        result.append(item)
    return result

# Статистика для каждого игрока рейтинга эффективности после 30 лет, отсортированная по среднем у рейтингу эффективности
def query9(collection):
    q = [
        {
            '$match': {
                 'Age': {'$gt': 30}
            }
        },
        {
            '$group': {
                '_id': '$Player',
                'max_PER': {'$max': '$PER'},
                'min_PER': {'$min': '$PER'},
                'avg_PER': {'$avg': '$PER'}
            }
        },
        {
            '$sort': {
                'avg_age': pymongo.DESCENDING
            }
        }
    ]
    data = collection.aggregate(q)
    result = []
    for item in data:
        result.append(item)
    return result

# Количество сезонов в карьере каждого игра с показателем рейтинга эффективности выше 25
def query10(collection):
    q = [
        {
            '$match': {
                'RSorPO': 'Regular Season',
                'PER': {'$gt': 25}
            }
        },
        {
            '$group': {
                '_id': '$Player',
                'count': {'$sum': 1}
            }
        }
    ]
    data = collection.aggregate(q)
    result = []
    for item in data:
        result.append(item)
    return result

# Удалить записи, у которых зарпалат меньше 600.000 или больше 33.000.000
def delete_by_salary(collection):
    return collection.delete_many({
        '$or': [
            {'Salary': {'$lt': 600_000}},
            {'Salary': {'$gt': 33_000_000}}
        ]
    })

# Увеличить процент блоков на 1 у всех
def inc_BLK(collection):
    return collection.update_many({}, {
        '$inc': {
            'BLK': 1
        }
    })

# Увеличение зарплаты на 5 процентов для всех атакующих защитников (SG)
def inc_salary(collection):
    return collection.update_many({
        'Pos': 'SG'
    }, {
        '$mul': {
            'salary': 1.05
        }
    })

# Увеличение зарплаты для Коби Брайанта на 7%
def inc_salary_for_Kobe(collection):
    return collection.update_many({
        'Player': 'Kobe Bryant'
    }, {
        '$mul': {
            'Salary': 1.07
        }
    })

def delete_by_age(collection):
    return collection.delete_many({
        '$or': [
            {'Age': {'$lt': 20}},
            {'Age': {'$gt': 35}}
        ]
    })

collection = connect_db()
# collection.insert_many(read_pkl('../data/4/salaries.pkl'))
# collection.insert_many(read_csv('../data/4/advanced_stats.csv'))

# ЗАПРОСЫ-ВЫВОДЫ
to_json('../result/result5.4.1.json', query1(collection))
to_json('../result/result5.4.2.json', query2(collection))
to_json('../result/result5.4.3.json', query3(collection))
to_json('../result/result5.4.4.json', query4(collection))
to_json('../result/result5.4.5.json', query5(collection))

# ЗАПРОСЫ-АГРЕГАЦИИ
to_json('../result/result5.4.6.json', query6(collection))
to_json('../result/result5.4.7.json', query7(collection))
to_json('../result/result5.4.8.json', query8(collection))
to_json('../result/result5.4.9.json', query9(collection))
to_json('../result/result5.4.10.json', query10(collection))

# ЗАПРОСЫ-МАНИПУЛЯЦИИ
# print(delete_by_salary(collection))
# print(inc_BLK(collection))
# print(inc_salary(collection))
# print(inc_salary_for_Kobe(collection))
# print(delete_by_age(collection))
import pymongo
from pymongo import MongoClient
import msgpack
import json
import pickle


def to_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Результат в формате json записан в {path}")

def connect_db():
    client = MongoClient()
    db = client["db-2024"]
    print(db.jobs)
    return db.jobs

def read_msgpack(path):
    with open(path, 'rb') as f:
        return msgpack.load(f)

def query11(collection):
    data = list(collection.find(limit=10).sort("salary", pymongo.DESCENDING))
    result = []
    for item in data:
        item.pop('_id', None)
        result.append(item)
    return result

def query12(collection):
    data = list(collection
                .find({'age': {'$lt': 30}}, limit=15)
                .sort("salary", pymongo.DESCENDING))
    result = []
    for item in data:
        item.pop('_id', None)
        result.append(item)
    return result

def query13(collection):
    data = list(collection
                .find({'city': 'Мурсия', 'job': {'$in': ['Архитектор', 'Программист', 'Учитель']}}, limit=10)
                .sort("age", pymongo.ASCENDING))
    result = []
    for item in data:
        item.pop('_id', None)
        result.append(item)
    return result

def query14(collection):
    return collection.count_documents({
        'age': {'$gt': 30, '$lte': 40},
        'year': {'$gt': 2019, '$lte': 2022},
        '$or': [
            {'salary': {'$gt': 50_000, '$lte': 75_000}},
            {'salary': {'$gt': 120_000, '$lte': 150_000}}
        ]
    })

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
                    if key == 'salary' or key == 'id' or key == 'year' or key == 'age':
                        value = int(value)
                    item[key] = value
        if item:
            items.append(item)
    return items

def query21(collection):
    q = [
        {
            '$group': {
                '_id': 'result',
                'max_salary': {'$max': '$salary'},
                'min_salary': {'$min': '$salary'},
                'avg_salary': {'$avg': '$salary'}
            }
        }
    ]
    data = collection.aggregate(q)
    result = []
    for item in data:
        item.pop('_id', None)
        result.append(item)
    return result

def query22(collection):
    q = [
        {
            '$group': {
                '_id': '$job',
                'count': {'$sum': 1}
            }
        }
    ]
    data = collection.aggregate(q)
    result = []
    for item in data:
        result.append(item)
    return result

def get_stat_by_custom_key(collection, group_by_key, agg_key):
    q = [
        {
            '$group': {
                '_id': f'${group_by_key}',
                f'max_{agg_key}': {'$max': f'${agg_key}'},
                f'min_{agg_key}': {'$min': f'${agg_key}'},
                f'avg_{agg_key}': {'$avg': f'${agg_key}'}
            }
        }
    ]
    data = collection.aggregate(q)
    result = []
    for item in data:
        result.append(item)
    return result

def query27(collection):
    q = [
        {
            '$group': {
                '_id': '$age',
                'max_salary': {'$max': '$salary'}
            }
        },
        {
            '$group': {
                '_id': '$result',
                'min_age': {'$min': '$_id'},
                'max_salary': {'$max': '$max_salary'}
            }
        }
    ]
    data = collection.aggregate(q)
    result = []
    for item in data:
        item.pop('_id', None)
        result.append(item)
    return result

def query28(collection):
    q = [
        {
            '$group': {
                '_id': '$salary',
                'max_age': {'$max': '$age'}
            }
        },
        {
            '$group': {
                '_id': '$result',
                'min_salary': {'$min': '$_id'},
                'max_age': {'$max': '$max_age'}
            }
        }
    ]
    data = collection.aggregate(q)
    result = []
    for item in data:
        item.pop('_id', None)
        result.append(item)
    return result

def query29(collection):
    q = [
        {
            '$match': {
                 'salary': {'$gt': 50_00}
            }
        },
        {
            '$group': {
                '_id': '$city',
                'max_age': {'$max': '$age'},
                'min_age': {'$min': '$age'},
                'avg_age': {'$avg': '$age'}
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

def query210(collection):
    q = [
        {
            '$match': {
                'city': {'$in': ['Виго', 'Бильбао', 'Бишкек', 'Камбадос']},
                'job': {'$in': ['Виго', 'Продавец', 'Психолог', 'Программист']},
                '$or': [
                    {'age': {'$gt': 18, '$lt': 25}},
                    {'age': {'$gt': 50, '$lt': 65}}
                ]
            }
        },
        {
            '$group': {
                '_id': 'result',
                'max_salary': {'$max': '$salary'},
                'min_salary': {'$min': '$salary'},
                'avg_salary': {'$avg': '$salary'}
            }
        }
    ]
    data = collection.aggregate(q)
    result = []
    for item in data:
        result.append(item)
    return result

def query211(collection):
    q = [
        {
            '$match': {
                 'year': {'$gt': 2002, '$lte': 2012}
            }
        },
        {
            '$group': {
                '_id': '$age',
                'max_salary': {'$max': '$salary'},
                'min_salary': {'$min': '$salary'},
                'avg_salary': {'$avg': '$salary'}
            }
        },
        {
            '$sort': {
                '_id': pymongo.ASCENDING
            }
        }
    ]
    data = collection.aggregate(q)
    result = []
    for item in data:
        result.append(item)
    return result

def read_pkl(path):
    with open(path, "rb") as file:
        data = pickle.load(file)
        return data

def delete_by_salary(collection):
    return collection.delete_many({
        '$or': [
            {'salary': {'$lt': 25_000}},
            {'salary': {'$gt': 175_000}}
        ]
    })

def inc_age(collection):
    return collection.update_many({}, {
        '$inc': {
            'age': 1
        }
    })

def inc_salary(collection):
    return collection.update_many({
        'job': {'$in': ['Повар', 'Программист', 'Учитель']}
    }, {
        '$mul': {
            'salary': 1.05
        }
    })

def inc_salary_for_city(collection):
    return collection.update_many({
        'city': {'$in': ['Астана', 'Куэнка', 'Сараево']}
    }, {
        '$mul': {
            'salary': 1.07
        }
    })

def complex_inc_salary(collection):
    return collection.update_many({
        'city': 'Москва',
        'job': {'$in': ['Архитектор', 'Программист', 'Повар']},
        'age': {'$gt': 18, '$lte': 65}
    }, {
        '$mul': {
            'salary': 1.10
        }
    })

def custom_delete(collection):
    return collection.delete_many({
        '$or': [
            {'age': {'$lt': 20}},
            {'age': {'$gt': 55}}
        ]
    })




# TASK 1

collection = connect_db()
# collection.insert_many(read_msgpack('../data/task_1_item.msgpack'))
# collection.insert_many(load_text('../data/task_2_item.text'))
# collection.insert_many(read_pkl('../data/task_3_item.pkl'))
to_json('../result/result5.1.1.json', query11(collection))
to_json('../result/result5.1.2.json', query12(collection))
to_json('../result/result5.1.3.json', query13(collection))
to_json('../result/result5.1.4.json', query14(collection))

# TASK 2

to_json('../result/result5.2.1.json', query21(collection))
to_json('../result/result5.2.2.json', query22(collection))
to_json('../result/result5.2.3.json', get_stat_by_custom_key(collection, 'city', 'salary'))
to_json('../result/result5.2.4.json', get_stat_by_custom_key(collection, 'job', 'salary'))
to_json('../result/result5.2.5.json', get_stat_by_custom_key(collection, 'city', 'age'))
to_json('../result/result5.2.6.json', get_stat_by_custom_key(collection, 'job', 'age'))
to_json('../result/result5.2.7.json', query27(collection))
to_json('../result/result5.2.8.json', query28(collection))
to_json('../result/result5.2.9.json', query29(collection))
to_json('../result/result5.2.10.json', query210(collection))
to_json('../result/result5.2.11.json', query211(collection))

#TASK 3

# delete_by_salary(collection)
# print(inc_age(collection))
# print(inc_salary(collection))
# print(inc_salary_for_city(collection))
# print(complex_inc_salary(collection))
# print(custom_delete(collection))
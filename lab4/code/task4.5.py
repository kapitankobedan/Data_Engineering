import pickle
import csv
from lab4.code.common import connect_to_db, to_json

def read_pkl(path):
    with open(path, "rb") as file:
        data = pickle.load(file)
        if 'Season' in data.columns:
            data['Season'] = data['Season'].str.split('-').str[0].astype(int)
        if 'Salary' in data.columns:
            data['Salary'] = data['Salary'].str.replace('$', '').astype(int)
        items = data.to_dict(orient="records")
        return items

def read_csv_for_second_table(path):
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
                'Player': row[27],
                'RSorPO': row[28]
            }
            for row in reader if row
        ]

def read_csv_for_third_table(path):
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        return [
            {
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
                'VORP': float(row[26])
            }
            for row in reader if row
        ]

def create_table1(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE "1_Salary" (
            id integer primary key,
            Season integer,
            Team text,
            Lg text,
            Salary integer,
            Player text)
    """)

def insert_data1(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO "1_Salary" (Season, Team, Lg, Salary, Player)
        VALUES (:Season, :Team, :Lg, :Salary, :Player)
    """, items)
    db.commit()

def create_table2(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE "2_Base" (
            id integer primary key,
            Season text,
            Age integer,
            Team text,
            Lg text,
            Pos text,
            G integer,
            MP integer,
            Player text,
            RSorPO text
            )
    """)

def insert_data2(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO "2_Base" (Season, Age, Team, Lg, Pos, G, MP, Player, RSorPO)
        VALUES (:Season, :Age, :Tm, :Lg, :Pos, :G, :MP, :Player, :RSorPO)
    """, items)
    db.commit()

def create_table3(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE "3_Stats" (
            id integer primary key,
            PER float,
            TS float,
            THPAr float,
            FTr float,
            ORB float,
            DRB float, 
            TRB float, 
            AST float,
            STL float,
            BLK float, 
            TOV float, 
            USG float, 
            OWS float, 
            DWS float,
            WS float, 
            WS48 float, 
            OBPM float, 
            DBPM float, 
            BPM float, 
            VORP float)
    """)

def insert_data3(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO "3_Stats" (PER, TS, THPAr, FTr, ORB, DRB, TRB, AST, STL, BLK, TOV, USG, OWS, DWS, WS, WS48, OBPM, DBPM, BPM, VORP)
        VALUES (:PER, :TS, :THPAr, :FTr, :ORB, :DRB, :TRB, :AST, :STL, :BLK, :TOV, :USG, :OWS, :DWS, :WS, :WS48, :OBPM, :DBPM, :BPM, :VORP)
    """, items)
    db.commit()

# Статиcтика по зарплате для каждого игрока за все сезоны: сумма, средняя, максимальная, минимальная
def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            Player, 
            SUM(Salary) as Sum_salary, 
            MIN(Salary) as Min_salary, 
            MAX(Salary) as Max_salary, 
            AVG(Salary) as AVG_salary 
        FROM "1_Salary"
        GROUP BY Player;
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

# Средняя зарплата игрока за один матч по сезонам
def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            Sal.Player AS Player, 
            Sal.Season AS Season, 
            SUM(Sal.Salary) / SUM(Base.G) AS Avg_salary_per_game
        FROM "1_Salary" AS Sal
        JOIN "2_Base" AS Base
        ON Sal.Player = Base.Player AND Sal.Season = Base.Season
        GROUP BY Sal.Player, Sal.Season;
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

# Сопоставление доли трёхочковых бросков на вклад в победы (среднее за РС и ПО)
def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            Base.Player AS Player, 
            Base.Season AS Season, 
            ROUND(AVG(Stats.THPAr),2 ) AS Avg_three_point_rate, 
            ROUND(AVG(Stats.WS), 2) AS Avg_win_shares
        FROM "3_Stats" AS Stats
        JOIN "2_Base" AS Base
        ON Stats.id = Base.id
        GROUP BY Base.Player, Base.Season;
    """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

# Процент заработной платы, приходящейся на один процент рейтинга эффективности (PER)
def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            Sal.Player AS Player, 
            Sal.Season AS Season, 
            Sal.Salary,
            Stats.PER,
            ROUND((Sal.Salary / Stats.PER), 2) AS Salary_per_efficiency
        FROM "1_Salary" AS Sal
        JOIN "2_Base" AS Base
            ON Sal.Player = Base.Player AND Sal.Season = Base.Season
        JOIN "3_Stats" AS Stats
            ON Base.id = Stats.id  
        WHERE Base.RSorPO = 'Regular Season'  
        GROUP BY Sal.Player, Sal.Season;
        """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

# Статистика игроков в регулярных сезонах относительно их возраста
def fifth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            Base.Age AS Age, 
            Base.Player AS Player,
            AVG(Stats.PER) AS PER,
            AVG(Stats.TS) AS True_Shooting_Percentage,
            AVG(Stats.TRB) AS Total_Rebound_Percentage,
            AVG(Stats.AST) AS Assist_Percentage,
            AVG(Stats.STL) AS Steal_Percentage,
            AVG(Stats.BLK) AS Block_Percentage,
            AVG(Stats.TOV) AS Turnover_Percentage,
            AVG(Stats.USG) AS Usage_Percentage,
            AVG(Stats.WS) AS Win_Shares
        FROM "3_Stats" AS Stats
        JOIN "2_Base" AS Base
            ON Stats.id = Base.id 
        WHERE Base.RSorPO = 'Regular Season'
        GROUP BY Base.Age, Base.Player
        ORDER BY Age;
        """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

# Вклад Коби Брайнта в победы по сезонам для регулярных матчей и ПО
def sixth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            Base.Season AS Season, 
            Base.RSorPO AS RS_or_PO,
            AVG(Stats.OWS) AS Offensive_impact, 
            AVG(Stats.DWS) AS Defensive_impact
        FROM "3_Stats" AS Stats
        JOIN "2_Base" AS Base
        ON Stats.id = Base.id
        WHERE Base.Player = 'Kobe Bryant'
        GROUP BY Base.Season, Base.RSorPO;
        """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items

# Средний процент трёхочковых бросков (THPAr) по игрокам за всю карьеру
def seventh_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            Base.Player AS Player, 
            ROUND(AVG(Stats.THPAr), 2) AS Avg_three_point_rate 
        FROM "3_Stats" AS Stats
        JOIN "2_Base" AS Base
        ON Stats.id = Base.id 
        GROUP BY Base.Player
        ORDER BY AVG(Stats.THPAr) DESC;
        """)
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    return items


# STEP 1
db = connect_to_db('../result/fourth.db')
# create_table1(db)
# create_table2(db)
# create_table3(db)
# STEP 2
# data1 = read_pkl(r'../data/5/salaries.pkl')
# data2 = read_csv_for_second_table(r'../data/5/advanced_stats.csv')
# data3 = read_csv_for_third_table(r'../data/5/advanced_stats.csv')
# insert_data1(db, data1)
# insert_data2(db, data2)
# insert_data3(db, data3)
# QUERY 1
to_json('../result/result4.5.1.json', first_query(db))
# QUERY 2
to_json('../result/result4.5.2.json', second_query(db))
# QUERY 3
to_json('../result/result4.5.3.json', third_query(db))
# QUERY 4
to_json('../result/result4.5.4.json', fourth_query(db))
# QUERY 5
to_json('../result/result4.5.5.json', fifth_query(db))
# QUERY 6
to_json('../result/result4.5.6.json', sixth_query(db))
# QUERY 7
to_json('../result/result4.5.7.json', seventh_query(db))
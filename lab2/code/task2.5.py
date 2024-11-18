import msgpack
import pickle
import pandas as pd
import os

df = pd.read_csv(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\data\IMDb movies.csv")

# print(df)

# print(df.columns)
new_df = df.drop(columns=['imdb_title_id', 'original_title', 'date_published', 'language', 'director', 'writer',
                      'production_company', 'actors', 'description', 'metascore', 'usa_gross_income',
                      'reviews_from_users', 'reviews_from_critics'])


# print(new_df.columns)

columns_to_clean = ['budget', 'worlwide_gross_income']


for column in columns_to_clean:
    new_df[column] = (
        new_df[column]
        .str.replace(r"[^\d.]", "", regex=True)  # Убираем всё, кроме цифр и точки
        .astype(float)  # Преобразуем в float
    )


import json

def find_indicators(new_df, numerical_columns, text_columns):
    info_columns = {}
    value_counts_json = {}

    for col in new_df.columns:
        if col in numerical_columns:
            info_columns[col] = {
                'maximal': float(new_df[col].max()),
                'minimal': float(new_df[col].min()),
                'total': float(new_df[col].sum()),
                'std': float(new_df[col].std()),
                'avg': float(new_df[col].mean())
            }

        if col in text_columns:
            all_values = new_df[col].str.split(', ').explode()
            value_counts = all_values.value_counts()
            value_counts_json[col] = value_counts.astype(int).to_dict()

    return info_columns, value_counts_json




# print(f"Column: {column}")
# print(f"Max: {maximal}, Min: {minimal}, Total: {total}, Std: {std}, Avg: {avg}")


numerical_columns = ['duration', 'avg_vote', 'votes', 'budget', 'worlwide_gross_income', 'year']
text_columns = ['genre', 'country']

result = find_indicators(new_df, numerical_columns, text_columns)

with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\result\result2.5.1.json", "w") as file:
    json.dump(result, file)
    print(f'Результат записан в result2.5.1.json')

df.to_json(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\result\result2.5.2.json")
print('Результат записан в result2.5.2.json')
with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\result\result2.5.3.msgpack", "wb") as file:
    packed = msgpack.packb(df.to_dict(), use_bin_type=True)
    file.write(packed)
    print('Результат записан в result2.5.3.msgpack')
# with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\result\result2.5.3.msgpack", "rb") as file:
#     unpacked = msgpack.unpackb(file.read(), strict_map_key=False, raw=False)  # raw=False для строк
#     print(unpacked)
with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\result\result2.5.4.pkl", "wb") as file:
    pickle.dump(df, file)
    print('Результат записан в result2.5.4.pkl')


first_size = os.path.getsize(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\data\IMDb movies.csv")
second_size = os.path.getsize(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\result\result2.5.2.json")
third_size = os.path.getsize(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\result\result2.5.3.msgpack")
fourth_size = os.path.getsize(r"C:\Users\Данила\PycharmProjects\DE_labs\lab2\result\result2.5.4.pkl")

print(f"csv = {first_size}\njson = {second_size}\nmsgpack = {third_size}\npkl = {fourth_size}")
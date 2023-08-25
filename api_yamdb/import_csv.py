import sqlite3
import csv

list_table = [
    {
        'file': 'c:/category.csv',
        'table': 'reviews_category',
        'fields': 'id, name, slug',
        'fields_num': '?,?,?'
    },
    {
        'file': 'c:/genre.csv',
        'table': 'reviews_genre',
        'fields': 'id, name, slug',
        'fields_num': '?,?,?'
    },
    {
        'file': 'c:/comments.csv',
        'table': 'reviews_comment',
        'fields': 'id, review_id, text, author, pub_date',
        'fields_num': '?,?,?,?,?'
    },
    {
        'file': 'c:/genre_title.csv',
        'table': 'reviews_genretitles',
        'fields': 'id, title_id, genre_id',
        'fields_num': '?,?,?'
    },
    {
        'file': 'c:/titles.csv',
        'table': 'reviews_titles',
        'fields': 'id, name, year, category',
        'fields_num': '?,?,?,?'
    },
    {
        'file': 'c:/users.csv',
        'table': 'auth_user',
        'fields': 'id, username, email, role, bio, first_name, last_name',
        'fields_num': '?,?,?,?,?,?,?'
    },
    {
        'file': 'c:/review.csv',
        'table': 'reviews_reviews',
        'fields': 'id, title_id, text, author, score, pub_date',
        'fields_num': '?,?,?,?,?,?'
    },
]


def import_csv(file, table, fields, fields_num):
    with open(f'{file}', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            try:
                sqlite_connection = sqlite3.connect('api_yamdb/db.sqlite3')
                cursor = sqlite_connection.cursor()
                print("Подключен к SQLite")

                sqlite_insert_query = f"""INSERT INTO {table}
                                        ({fields})
                                        VALUES
                                        ({fields_num});"""   
                data_tuple = row
                cursor.execute(sqlite_insert_query, data_tuple)
                sqlite_connection.commit()
                print(f"Запись успешно вставлена ​​в таблицу {table} ", cursor.rowcount)
                cursor.close()
            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")


def delete_record(table):
    try:
        sqlite_connection = sqlite3.connect('api_yamdb/db.sqlite3')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_delete_query = f"""DELETE from {table}"""
        cursor.execute(sql_delete_query)
        sqlite_connection.commit()
        print(f"В таблице {table} записи успешно удалены")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


for i in range(0, len(list_table)):
    delete_record(list_table[i]['table'])
    import_csv(list_table[i]['file'], list_table[i]['table'], list_table[i]['fields'], list_table[i]['fields_num'])

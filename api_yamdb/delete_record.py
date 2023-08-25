import sqlite3
import csv

list_table = ('reviews_genre', )

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
    delete_record(list_table[i])




# try:
#     sqlite_connection = sqlite3.connect('api_yamdb/db.sqlite3')
#     cursor = sqlite_connection.cursor()
#     print("Подключен к SQLite")

#     sqlite_insert_query = f"""INSERT INTO {table}
#                             ({fields})
#                             VALUES
#                             ({fields_num});"""   
#     data_tuple = row
#     cursor.execute(sqlite_insert_query, data_tuple)
#     sqlite_connection.commit()
#     print(f"Запись успешно вставлена ​​в таблицу {table} ", cursor.rowcount)
#     cursor.close()
# except sqlite3.Error as error:
#     print("Ошибка при работе с SQLite", error)
# if sqlite_connection:
#     sqlite_connection.close()
#     print("Соединение с SQLite закрыто")
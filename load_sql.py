import os
import django
import sqlite3


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


db_path = 'db.sqlite3'
sql_file = 'fill_db.sql'


conn = sqlite3.connect(db_path)
cursor = conn.cursor()


with open(sql_file, 'r', encoding='utf-8') as file:
    sql_script = file.read()


cursor.executescript(sql_script)

conn.commit()
conn.close()

print("Данные успешно загружены в базу данных.")

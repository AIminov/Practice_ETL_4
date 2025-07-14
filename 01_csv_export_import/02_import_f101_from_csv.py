# 01_csv_export_import/02_import_f101_from_csv.py

import psycopg2
import csv
import os
import yaml

# Чтение конфигурации подключения
with open('01_csv_export_import/config.yaml') as f:
    config = yaml.safe_load(f)

DB_PARAMS = config['db']
SCRIPT_NAME = '02_import_f101_from_csv.py'
CSV_FILE = '01_csv_export_import/dm_f101_round_f.csv'
TABLE_NAME = 'dm.dm_f101_round_f_v2'

try:
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    # Чтение CSV
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)

    # Очистка целевой таблицы
    cursor.execute(f"DELETE FROM {TABLE_NAME};")

    # Подготовка и выполнение вставки
    placeholders = ', '.join(['%s'] * len(headers))
    insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(headers)}) VALUES ({placeholders})"
    for row in rows:
        cursor.execute(insert_sql, row)

    # Логирование успеха
    cursor.execute("""
        INSERT INTO logs.etl_stdout_log (script_name, step, message)
        VALUES (%s, %s, %s);
    """, (SCRIPT_NAME, 'IMPORT', f'{len(rows)} rows imported into {TABLE_NAME}'))

    conn.commit()

except Exception as e:
    # Логирование ошибки
    cursor.execute("""
        INSERT INTO logs.etl_stdout_log (script_name, step, message)
        VALUES (%s, %s, %s);
    """, (SCRIPT_NAME, 'ERROR', str(e)))
    conn.commit()
    raise

finally:
    cursor.close()
    conn.close()

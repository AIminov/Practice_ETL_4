import psycopg2
import csv
import yaml
import os

CSV_FILE = '01_csv_export_import/dm_f101_round_f.csv'
SCRIPT_NAME = '01_export_f101_to_csv.py'

# загружаем параметры подключения
with open('01_csv_export_import/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
DB_PARAMS = config['db']

conn = None
cursor = None

try:
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dm.dm_f101_round_f ORDER BY from_date, ledger_account;")
    rows = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]

    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(colnames)
        writer.writerows(rows)

    cursor.execute("""
        INSERT INTO logs.etl_stdout_log (script_name, step, message)
        VALUES (%s, %s, %s);
    """, (SCRIPT_NAME, 'EXPORT', f'Exported {len(rows)} rows to {CSV_FILE}'))
    conn.commit()

except Exception as e:
    if conn and cursor:
        cursor.execute("""
            INSERT INTO logs.etl_stdout_log (script_name, step, message)
            VALUES (%s, %s, %s);
        """, (SCRIPT_NAME, 'ERROR', str(e)))
        conn.commit()
    raise

finally:
    if cursor: cursor.close()
    if conn: conn.close()

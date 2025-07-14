#!/bin/bash

set -e

export PGCLIENTENCODING=UTF8
export LANG=ru_RU.UTF-8

echo "[STEP 0] создаем таблицу логов (если еще нет)"
psql -U postgres -d postgres -f ./00_ddl/01_logs.etl_stdout_log.sql

echo "[STEP 1] создаем копию витрины dm.dm_f101_round_f_v2"
psql -U postgres -d postgres -f ./00_ddl/02_dm.dm_f101_round_f_v2.sql

echo "[STEP 2] экспорт данных из формы 101 в CSV"
python3 ./01_csv_export_import/01_export_f101_to_csv.py

echo "[MANUAL] отредактируйте CSV-файл и нажмите [ENTER] для продолжения"
read

echo "[STEP 3] импорт данных из CSV в dm_f101_round_f_v2"
python3 ./01_csv_export_import/02_import_f101_from_csv.py

echo "[DONE] выполнение завершено"

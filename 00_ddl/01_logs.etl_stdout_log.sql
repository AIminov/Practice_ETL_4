CREATE TABLE IF NOT EXISTS logs.etl_stdout_log (
    log_dt         TIMESTAMP DEFAULT clock_timestamp(),
    script_name    TEXT,
    step           TEXT,
    message        TEXT
);
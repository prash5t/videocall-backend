import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect('videocall_logs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS call_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  call_id TEXT,
                  caller_email TEXT,
                  callee_email TEXT,
                  start_time DATETIME,
                  end_time DATETIME,
                  status TEXT,
                  duration INTEGER)''')
    conn.commit()
    conn.close()


def log_call(call_id, caller_email, callee_email, status, start_time=None, end_time=None):
    conn = sqlite3.connect('videocall_logs.db')
    c = conn.cursor()
    duration = None
    if start_time and end_time:
        duration = (end_time - start_time).total_seconds()
    c.execute('''INSERT INTO call_logs (call_id, caller_email, callee_email, start_time, end_time, status, duration)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (call_id, caller_email, callee_email, start_time, end_time, status, duration))
    conn.commit()
    conn.close()


def get_call_logs():
    conn = sqlite3.connect('videocall_logs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM call_logs ORDER BY start_time DESC')
    logs = c.fetchall()
    conn.close()
    return logs

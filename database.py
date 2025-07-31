import sqlite3
import time

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    start_time INTEGER,
    subscribed BOOLEAN DEFAULT 0
)
''')
conn.commit()

def add_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (user_id, start_time) VALUES (?, ?)", (user_id, int(time.time())))
    conn.commit()

def is_trial_active(user_id):
    cursor.execute("SELECT start_time, subscribed FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    if not data:
        return False
    start_time, subscribed = data
    if subscribed:
        return True
    return (int(time.time()) - start_time) <= 3600  # 1 час

def activate_subscription(user_id):
    cursor.execute("UPDATE users SET subscribed = 1 WHERE user_id = ?", (user_id,))
    conn.commit()

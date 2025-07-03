import sqlite3

conn = sqlite3.connect("users.db")

conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    age INTEGER,
    class_batch TEXT,
    profile_pic TEXT,
    password TEXT,
    is_admin INTEGER DEFAULT 0
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    project_title TEXT,
    github_url TEXT,
    is_approved INTEGER DEFAULT 0,
    cert_file TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

conn.commit()
conn.close()
print("✅ Tables 'users' and 'projects' created in users.db")

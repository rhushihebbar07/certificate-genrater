import sqlite3

# Path to your DB file
db_path = "users.db"  # change if it's a different name

# Connect to DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Run the cleanup SQL
cursor.execute("""
    UPDATE projects
    SET project_title = REPLACE(REPLACE(REPLACE(project_title, '—', '-'), '–', '-'), '‑', '-')
    WHERE id = 37
""")

conn.commit()
print("✅ Cleaned project_title for ID 37.")
conn.close()

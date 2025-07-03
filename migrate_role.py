from app import get_db_connection

conn = get_db_connection()
conn.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student'")
conn.commit()
conn.close()

print("✅ 'role' column added to users table.")

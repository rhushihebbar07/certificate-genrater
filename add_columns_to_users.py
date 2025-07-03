import sqlite3

DATABASE = "users.db"  # ✅ Adjust this if needed

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# 🔄 Add 'role' column if it doesn't exist
try:
    cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student'")
    print("✅ Added 'role' column.")
except sqlite3.OperationalError as e:
    print("⚠️ 'role' column may already exist:", e)

# 🔄 Add 'is_superadmin' column if it doesn't exist
try:
    cursor.execute("ALTER TABLE users ADD COLUMN is_superadmin INTEGER DEFAULT 0")
    print("✅ Added 'is_superadmin' column.")
except sqlite3.OperationalError as e:
    print("⚠️ 'is_superadmin' column may already exist:", e)

conn.commit()
conn.close()

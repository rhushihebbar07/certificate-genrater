import sqlite3

DATABASE = "users.db"

conn = sqlite3.connect(DATABASE)
conn.execute("UPDATE users SET role = 'admin', is_superadmin = 1 WHERE email = 'admin@smscollege.edu'")
conn.commit()
conn.close()

print("✅ Super admin set for admin@smscollege.edu")

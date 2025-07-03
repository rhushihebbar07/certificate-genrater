import sqlite3

conn = sqlite3.connect("your_database_name.db")  # Replace with your actual DB path
conn.execute("UPDATE users SET role = 'admin', is_superadmin = 1 WHERE email = 'admin@smscollege.edu'")
conn.commit()
conn.close()

print("✅ Super Admin set successfully.")

import sqlite3

conn = sqlite3.connect('instance/placement.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE student ADD COLUMN education VARCHAR(200)")
    cursor.execute("ALTER TABLE student ADD COLUMN skills VARCHAR(200)")
    conn.commit()
    print("Database upgraded successfully! Added education and skills columns.")
except sqlite3.OperationalError as e:
    print(f"Notice: {e} (The columns might already exist!)")

conn.close()
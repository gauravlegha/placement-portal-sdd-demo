import sqlite3

# Connect to your existing database
conn = sqlite3.connect('instance/placement.db')
cursor = conn.cursor()

# List of columns that might be missing in the 'company' table
columns_to_add = [
    "ALTER TABLE company ADD COLUMN is_blacklisted BOOLEAN DEFAULT 0",
    "ALTER TABLE company ADD COLUMN hr_contact VARCHAR(100)",
    "ALTER TABLE company ADD COLUMN website VARCHAR(100)"
]

for query in columns_to_add:
    try:
        cursor.execute(query)
        conn.commit()
        print(f"Successfully added column via: {query}")
    except sqlite3.OperationalError as e:
        # If the column already exists, SQLite throws an error, which we can safely ignore
        print(f"Notice: {e} -> Skipping (column likely already exists).")

conn.close()
print("Database upgrade complete!")
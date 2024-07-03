import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("test.db")
cursor = conn.cursor()


cursor.execute("""
               CREATE TABLE tips (
                   id INTEGER PRIMARY KEY,
                   title TEXT NOT NULL,
                   content TEXT NOT NULL,
                   category TEXT,
                   date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   author TEXT DEFAULT mapache
               )
               """)


conn.commit()
conn.close()

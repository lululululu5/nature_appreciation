import sqlite3
import json

DATABASE = 'sustainability_tips.db'

with open('sustainability_tips.json') as f:
    tips = json.load(f)


def insert_tips(tips):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    for tip in tips:
        cursor.execute("""
            INSERT INTO tips (title, content, category)
            VALUES (?, ?, ?)
        """, (tip['title'], tip['content'], tip['category']))

    conn.commit()
    conn.close()


# Insert tips into the database
insert_tips(tips)

print("Tips have been successfully uploaded to the database.")

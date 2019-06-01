
import sqlite3 as lite

conn = lite.connect('bink_datasets.db')
cur = conn.cursor()

def get_posts():
    with conn:
        cur.execute("SELECT Name FROM bink_datasets")
        print(cur.fetchall())

get_posts()
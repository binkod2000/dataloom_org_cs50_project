import numpy as np
import pandas as pd

import csv, sqlite3

con = sqlite3.connect("bink_datasets")
cur = con.cursor()
cur.execute("CREATE TABLE t (Date, Draw, 1, 2, 3, 4, 5,	6, 	7, 	8, 	9, 	10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, Mult, Bullseye);") # use your column names here

with open('keno2.csv','rb') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['col1'], i['col2']) for i in dr]

cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
con.commit()
con.close()


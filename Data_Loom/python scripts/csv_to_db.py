import numpy as np
import pandas as pd
import sqlite3
from cs50 import SQL

def import_csv_to_database(database, csv, table_name):
    db = sqlite3.connect(database)
    if not db:
        print('Could not connect to the database')
    # Read CSV file into a Pandas dataframe
    df = pd.read_csv(csv)

    # Insert the dataframe into the database as a table
    df.to_sql(con=db, name=table_name, if_exists='replace', flavor='sqlite')


    print('{}'.format(df))

database = input('What database would you like to connect to?')
csv = input('What csv would you like to import?')
table_name = input('What would you like to name the table?')


import_csv_to_database(database, csv, table_name)



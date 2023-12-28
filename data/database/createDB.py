import sqlite3
import pandas as pd

df = pd.read_csv('goldonlydb.csv')
df.columns = df.columns.str.strip()

connection = sqlite3.connect('olympicsDB.db')

df.to_sql('GoldOnlyDB', connection, if_exists='replace')

connection.close()
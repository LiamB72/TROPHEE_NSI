import sqlite3
import pandas as pd

df = pd.read_csv('athlete_events.csv')
df.columns = df.columns.str.strip()

connection = sqlite3.connect('olympicsDB.db')

df.to_sql('olympicsDB', connection, if_exists='replace')

connection.close()
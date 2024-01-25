"""
File Created By BERGE Liam
Created on 2024-01-08
Last Update on 2024-01-25
"""
import sqlite3
import pandas as pd

df = pd.read_csv('athlete_events.csv')
df.columns = df.columns.str.strip()

connection = sqlite3.connect('olympicsDB.db')

df.to_sql('olympicsDB', connection, if_exists='replace')

connection.close()
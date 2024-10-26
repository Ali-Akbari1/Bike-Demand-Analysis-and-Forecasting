import pandas as pd
import sqlite3

data = pd.read_csv('SeoulBikeData.csv')

conn = sqlite3.connect('bike_sharing.db')
data.to_sql()
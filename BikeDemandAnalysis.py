import pandas as pd
import sqlite3
import numpy as np


data = pd.read_csv('SeoulBikeData.csv', encoding='ISO-8859-1')


conn = sqlite3.connect('bike_sharing.db')
data.to_sql('bike_data', conn, if_exists='replace', index=False)
conn.commit()

## print(data.columns)

create_view_query = """
CREATE VIEW IF NOT EXISTS daily_avg_rentals AS
SELECT 
    DATE(Date) as day, 
    AVG(Rented_Bike_Count) as avg_rentals,
    AVG(Temperature) as avg_temp,
    AVG(Humidity) as avg_humidity
FROM bike_data
GROUP BY day;
"""



# Execute the SQL query
conn.execute(create_view_query)
daily_avg_rentals = pd.read_sql("SELECT * FROM daily_avg_rentals", conn)

# Categorize temperature
daily_avg_rentals['temp_category'] = pd.cut(daily_avg_rentals['avg_temp'], bins=[-10, 10, 20, 35], labels=['Low', 'Medium', 'High'])

# Check average rentals for each temperature category
rentals_by_temp = daily_avg_rentals.groupby('temp_category', observed=False)['avg_rentals'].mean()

# Filter out NaN values
rentals_by_temp = rentals_by_temp.dropna()

print(rentals_by_temp)

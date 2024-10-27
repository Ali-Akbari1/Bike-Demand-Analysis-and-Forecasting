import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('SeoulBikeData.csv', encoding='ISO-8859-1')


# Add temperature category column
def categorize_temperature(temp):
    if temp < 0:
        return 'Cold (< 0°C)'
    elif 0 <= temp < 10:
        return 'Cool (0°C - 9°C)'
    elif 10 <= temp < 20:
        return 'Mild (10°C - 19°C)'
    elif 20 <= temp < 30:
        return 'Warm (20°C - 29°C)'
    else:
        return 'Hot (>=30°C)'

data['Temperature_Category'] = data['Temperature'].apply(categorize_temperature)

conn = sqlite3.connect('bike_sharing.db')
data.to_sql('bike_data', conn, if_exists='replace', index=False)
conn.commit()

# Calculate average rentals by temperature category and create a new view
create_avg_rentals_by_temp_view = """
CREATE VIEW IF NOT EXISTS avg_rentals_by_temp AS
SELECT 
    Temperature_Category,
    AVG(Rented_Bike_Count) AS avg_rentals
FROM bike_data
GROUP BY Temperature_Category
"""

create_avg_rentals_by_seasons = """
CREATE VIEW IF NOT EXISTS avg_rentals_by_seasons AS
SELECT
    Seasons,
    AVG(Rented_Bike_Count) AS avg_rentals
FROM bike_data
GROUP BY Seasons;
"""

conn.execute(create_avg_rentals_by_temp_view)
conn.execute(create_avg_rentals_by_seasons)

# Fetch the results into a DataFrame for viewing
avg_rentals_by_temp = pd.read_sql("""
SELECT * 
FROM avg_rentals_by_temp
ORDER BY 
    CASE 
        WHEN Temperature_Category = 'Cold (< 0°C)' THEN 1
        WHEN Temperature_Category = 'Cool (0°C - 9°C)' THEN 2
        WHEN Temperature_Category = 'Mild (10°C - 19°C)' THEN 3
        WHEN Temperature_Category = 'Warm (20°C - 29°C)' THEN 4
        WHEN Temperature_Category = 'Hot (>=30°C)' THEN 5
    END;
""", conn)
print(avg_rentals_by_temp)

avg_rentals_by_seasons = pd.read_sql("""
SELECT * 
FROM avg_rentals_by_seasons
ORDER BY 
    CASE
        WHEN Seasons = 'Autumn' THEN 1
        WHEN Seasons = 'Winter' THEN 2
        WHEN Seasons = 'Spring' THEN 3
        WHEN Seasons = 'Summer' THEN 4
    END;
""", conn)
print(avg_rentals_by_seasons)

# Close the connection when done
conn.close()

# Plotting average rentals by temperature category
plt.figure(figsize=(10, 5))  # Set the figure size
plt.bar(avg_rentals_by_temp['Temperature_Category'], avg_rentals_by_temp['avg_rentals'], color='skyblue')
plt.title('Average Bike Rentals by Temperature')
plt.xlabel('Temperature Category')
plt.ylabel('Average Rentals')
plt.grid(axis='y')  # Add gridlines for better readability
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()  # Display the plot

# Plotting average rentals by seasons
plt.figure(figsize=(10, 5))  # Set the figure size
plt.bar(avg_rentals_by_seasons['Seasons'], avg_rentals_by_seasons['avg_rentals'], color='lightgreen')
plt.title('Average Bike Rentals by Season')
plt.xlabel('Season')
plt.ylabel('Average Rentals')
plt.grid(axis='y')  # Add gridlines for better readability
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()  # Display the plot
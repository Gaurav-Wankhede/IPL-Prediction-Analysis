import pyodbc
from Prev_Matches.MVP_Data import final_data

# Define your SQL Server connection parameters
server = r'DESKTOP-F8QC9QH\SQLEXPRESS'
database = r'Realtime_IPL_Prediction'

# Connect to the database
conn = pyodbc.connect(r'DRIVER={SQL Server};'
                      r'SERVER=' + server + ';'
                      r'DATABASE=' + database + ';'
                      r'Trusted_Connection=yes;')

# Create a cursor
cursor = conn.cursor()

# Create MVP_Data table if it doesn't exist
if not cursor.tables(table='MVP_Data', tableType='TABLE').fetchone():
    cursor.execute('''
        CREATE TABLE MVP_Data (
            MVP_ID int IDENTITY(1,1) PRIMARY KEY,
            Player_Name VARCHAR(255),
            Team VARCHAR(255),
            Total_Impact INT,
            Runs INT,
            Impact_Runs INT,
            Batting_Impact INT,
            Bowl INT,
            Impact_Wickets INT,
            Bowling_Impact INT
        )
    ''')

# Iterate through the rows of the final_data DataFrame and insert or update records in the database
for index, row in final_data.iterrows():
    # Check if the row already exists in the database
    cursor.execute('''
        SELECT * FROM MVP_Data 
        WHERE Player_Name = ? AND Team = ?
    ''', row["Player_Name"], row["Team"])
    existing_row = cursor.fetchone()

    # If the row exists, update it
    if existing_row:
        cursor.execute('''
            UPDATE MVP_Data 
            SET Total_Impact = ?,
                Runs = ?,
                Impact_Runs = ?,
                Batting_Impact = ?,
                Bowl = ?,
                Impact_Wickets = ?,
                Bowling_Impact = ?
            WHERE MVP_ID = ?
        ''', row["Total_Impact"], row["Runs"], row["Impact_Runs"], row["Batting_Impact"],
           row["Bowl"], row["Impact_Wickets"], row["Bowling_Impact"], existing_row[0])
    else:
        # If the row does not exist, insert it
        cursor.execute('''
            INSERT INTO MVP_Data (Player_Name, Team, Total_Impact, Runs, Impact_Runs, Batting_Impact, Bowl, Impact_Wickets, Bowling_Impact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', row["Player_Name"], row["Team"], row["Total_Impact"], row["Runs"], row["Impact_Runs"],
           row["Batting_Impact"], row["Bowl"], row["Impact_Wickets"], row["Bowling_Impact"])

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

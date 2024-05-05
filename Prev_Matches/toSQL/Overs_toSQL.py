import pyodbc
from Prev_Matches.Overs import df

# Define your SQL Server connection parameters
server = r'DESKTOP-F8QC9QH\SQLEXPRESS'
database = r'IPL_Prediction_Analysis'

# Connect to the database
conn = pyodbc.connect(r'DRIVER={SQL Server};'
                      r'SERVER=' + server + ';'
                      r'DATABASE=' + database + ';'
                      r'Trusted_Connection=yes;')

# Create a cursor
cursor = conn.cursor()

# Create Overs_Data table if it doesn't exist
if not cursor.tables(table='Overs_Data', tableType='TABLE').fetchone():
    cursor.execute('''
        CREATE TABLE Overs_Data (
            Overs_ID INT PRIMARY KEY,
            Innings VARCHAR(255),
            Venue VARCHAR(255),
            Date DATE,
            Team_Name VARCHAR(255),
            Overs VARCHAR(255),
            Team_Runs INT,
            Team_Wickets INT,
            Team_Total_Runs INT,
            Team_Total_Wickets INT
        )
    ''')

# Iterate through the rows of the DataFrame and insert or update records in the database
for index, row in df.iterrows():
    # Check if the row already exists in the database
    cursor.execute('''
        SELECT * FROM Overs_Data WHERE Overs_ID = ? AND Innings = ? AND Venue = ? AND Date = ? AND Team_Name = ?
    ''', (row['Over_ID'], row['Innings'], row['Venue'], row['Date'], row['Team_Name']))
    existing_row = cursor.fetchone()

    # If the row exists, update it
    if existing_row:
        cursor.execute('''
            UPDATE Overs_Data 
            SET
                Overs = ?,
                Team_Runs = ?,
                Team_Wickets = ?,
                Team_Total_Runs = ?,
                Team_Total_Wickets = ?
            WHERE 
                Overs_ID = ? AND Innings = ? AND Venue = ? AND Date = ? AND Team_Name = ?
        ''', (row['Overs'], row['Team_Runs'], row['Team_Wickets'], row['Team_Total_Runs'], row['Team_Total_Wickets'],
              row['Over_ID'], row['Innings'], row['Venue'], row['Date'], row['Team_Name']))
    else:
        # If the row does not exist, insert it
        cursor.execute('''
            INSERT INTO Overs_Data 
                (Overs_ID, Innings, Venue, Date, Team_Name, Overs, Team_Runs, Team_Wickets, Team_Total_Runs, Team_Total_Wickets)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['Over_ID'], row['Innings'], row['Venue'], row['Date'], row['Team_Name'], row['Overs'], row['Team_Runs'],
              row['Team_Wickets'], row['Team_Total_Runs'], row['Team_Total_Wickets']))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

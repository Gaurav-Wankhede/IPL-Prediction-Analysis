import pyodbc
from Latest_Matches.Latest_Stats import df

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

# Create Stats_Data table if it doesn't exist
cursor.execute("""
    IF OBJECT_ID('Stats_Data', 'U') IS NULL
    CREATE TABLE Stats_Data (
        Stats_ID INT,
        Innings VARCHAR(255),
        Venue VARCHAR(255),
        Date DATE,
        Team VARCHAR(255),
        Player1 VARCHAR(255),
        Player2 VARCHAR(255),
        Player1_Runs INT,
        Player1_Balls INT,
        Partnership_Runs INT,
        Partnership_Balls INT,
        Player2_Runs INT,
        Player2_Balls INT
    )
""")

# Iterate through the rows of the final_data DataFrame and insert or update records in the database
for index, row in df.iterrows():
    # Check if the row already exists in the database
    cursor.execute("""
        SELECT * FROM Stats_Data WHERE Stats_ID = ?
    """, row['Stats_ID'])

    existing_row = cursor.fetchone()

    # If the row exists, update it
    if existing_row:
        cursor.execute("""
            UPDATE Stats_Data
            SET Innings = ?, Venue = ?, Date = ?, Team = ?, Player1 = ?, Player2 = ?, Player1_Runs = ?, Player1_Balls = ?, Partnership_Runs = ?, Partnership_Balls = ?, Player2_Runs = ?, Player2_Balls = ?
            WHERE Stats_ID = ?
        """, row['Innings'], row['Venue'], row['Date'], row['Team'], row['Player1'], row['Player2'], row['Player1_Runs'], row['Player1_Balls'], row['Partnership_Runs'], row['Partnership_Balls'], row['Player2_Runs'], row['Player2_Balls'], row['Stats_ID'])
    else:
        # If the row does not exist, insert it
        cursor.execute("""
            INSERT INTO Stats_Data (Stats_ID, Innings, Venue, Date, Team, Player1, Player2, Player1_Runs, Player1_Balls, Partnership_Runs, Partnership_Balls, Player2_Runs, Player2_Balls)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row['Stats_ID'], row['Innings'], row['Venue'], row['Date'], row['Team'], row['Player1'], row['Player2'], row['Player1_Runs'], row['Player1_Balls'], row['Partnership_Runs'], row['Partnership_Balls'], row['Player2_Runs'], row['Player2_Balls'])

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

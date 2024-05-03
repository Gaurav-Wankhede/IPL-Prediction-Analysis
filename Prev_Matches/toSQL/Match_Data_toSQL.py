import pyodbc
from Prev_Matches.Match_data import all_matches_data  # Import the DataFrame

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

# Check if the table already exists and create it if not
if not cursor.tables(table='Match_Data', tableType='TABLE').fetchone():
    cursor.execute('''
        CREATE TABLE Match_Data (
            Match_ID int IDENTITY(1,1) PRIMARY KEY,
            Innings nvarchar(255),
            Venue nvarchar(255),
            Date nvarchar(255),
            Team1 nvarchar(255),
            Team2 nvarchar(255),
            Team1_runs int,
            Team1_wickets int,
            Team2_runs int,
            Team2_wickets int,
            Target int,
            Team1_played_Overs nvarchar(255),
            Team2_played_Overs nvarchar(255),
            Match_Result nvarchar(255)
        )
    ''')
    print("Table 'Match_Data' created successfully.")
    conn.commit()

# Iterate over each row in the DataFrame
for index, row in all_matches_data.iterrows():
    # Convert the row to a list to access elements by index
    row_list = row.tolist()

    # Check if the row already exists in the database
    cursor.execute('''
        SELECT * FROM Match_Data 
        WHERE Innings = ? AND Venue = ? AND Date = ? AND Team1 = ? AND Team2 = ?
    ''', row_list[0], row_list[1], row_list[2], row_list[3], row_list[4])

    existing_row = cursor.fetchone()

    # If the row exists, update it
    if existing_row:
        cursor.execute('''
            UPDATE Match_Data 
            SET Team1_runs = ?, Team1_wickets = ?, Team2_runs = ?, Team2_wickets = ?, Target = ?, Team1_played_Overs = ?, Team2_played_Overs = ?, Match_Result = ?
            WHERE Match_ID = ?
        ''', row_list[5], row_list[6], row_list[7], row_list[8], row_list[9], row_list[10], row_list[11], row_list[12], existing_row.Match_ID)
        print(f"Values updated for match: {row_list[0]} {row_list[1]} {row_list[2]} {row_list[3]} {row_list[4]}")
    else:
        # If the row does not exist, insert it
        cursor.execute('''
            INSERT INTO Match_Data (Innings, Venue, Date, Team1, Team2, Team1_runs, Team1_wickets, Team2_runs, Team2_wickets, Target, Team1_played_Overs, Team2_played_Overs, Match_Result)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', row_list[0], row_list[1], row_list[2], row_list[3], row_list[4], row_list[5], row_list[6], row_list[7], row_list[8], row_list[9], row_list[10], row_list[11], row_list[12])
        print(f"Values inserted for match: {row_list[0]} {row_list[1]} {row_list[2]} {row_list[3]} {row_list[4]}")

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

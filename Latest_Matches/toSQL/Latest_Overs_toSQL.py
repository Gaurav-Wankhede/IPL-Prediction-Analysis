def latest_overs_sql():
    import sqlite3
    from Latest_Matches.Latest_Overs import latest_overs

    # Specify the absolute path to the database file
    db_file = "../../database/IPL_Prediction_Analysis.db"

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Create a cursor
    cursor = conn.cursor()

    # Define the table name
    table_name = 'Overs_Data'

    # Check if the table already exists and create it if not
    cursor.execute(f'''
        SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'
    ''')
    existing_table = cursor.fetchone()

    if not existing_table:
        cursor.execute('''
            CREATE TABLE Overs_Data (
                Overs_ID INTEGER PRIMARY KEY,
                Innings TEXT,
                Venue TEXT,
                Date TEXT,
                Team_Name TEXT,
                Overs TEXT,
                Team_Runs INTEGER,
                Team_Wickets INTEGER,
                Team_Total_Runs INTEGER,
                Team_Total_Wickets INTEGER
            )
        ''')

    df = latest_overs()

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

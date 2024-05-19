def latest_stats_sql():
    import sqlite3
    from Latest_Matches.Latest_Stats import latest_stats

    # Specify the absolute path to the SQLite database file
    db_file = "../../database/IPL_Prediction_Analysis.db"

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Create a cursor
    cursor = conn.cursor()

    # Define the table name
    table_name = 'Stats_Data'

    # Check if the table already exists and create it if not
    cursor.execute(f'''
        SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'
    ''')
    existing_table = cursor.fetchone()

    if not existing_table:
        cursor.execute('''
            CREATE TABLE Stats_Data (
                Stats_ID INTEGER PRIMARY KEY,
                Innings TEXT,
                Venue TEXT,
                Date TEXT,
                Team TEXT,
                Player1 TEXT,
                Player2 TEXT,
                Player1_Runs INTEGER,
                Player1_Balls INTEGER,
                Partnership_Runs INTEGER,
                Partnership_Balls INTEGER,
                Player2_Runs INTEGER,
                Player2_Balls INTEGER
            )
        ''')

    df = latest_stats()

    # Iterate through the rows of the DataFrame and insert or update records in the database
    for index, row in df.iterrows():
        # Check if the row already exists in the database
        cursor.execute('''
            SELECT * FROM Stats_Data WHERE Stats_ID = ?
        ''', row['Stats_ID'])

        existing_row = cursor.fetchone()

        # If the row exists, update it
        if existing_row:
            cursor.execute('''
                UPDATE Stats_Data
                SET Innings = ?, Venue = ?, Date = ?, Team = ?, Player1 = ?, Player2 = ?, Player1_Runs = ?, Player1_Balls = ?, Partnership_Runs = ?, Partnership_Balls = ?, Player2_Runs = ?, Player2_Balls = ?
                WHERE Stats_ID = ?
            ''', (row['Innings'], row['Venue'], row['Date'], row['Team'], row['Player1'], row['Player2'], row['Player1_Runs'], row['Player1_Balls'], row['Partnership_Runs'], row['Partnership_Balls'], row['Player2_Runs'], row['Player2_Balls'], row['Stats_ID']))
        else:
            # If the row does not exist, insert it
            cursor.execute('''
                INSERT INTO Stats_Data (Stats_ID, Innings, Venue, Date, Team, Player1, Player2, Player1_Runs, Player1_Balls, Partnership_Runs, Partnership_Balls, Player2_Runs, Player2_Balls)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row['Stats_ID'], row['Innings'], row['Venue'], row['Date'], row['Team'], row['Player1'], row['Player2'], row['Player1_Runs'], row['Player1_Balls'], row['Partnership_Runs'], row['Partnership_Balls'], row['Player2_Runs'], row['Player2_Balls']))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

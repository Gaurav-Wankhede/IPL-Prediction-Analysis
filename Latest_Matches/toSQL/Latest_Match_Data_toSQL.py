def latest_match_data_sql():
    import sqlite3
    from Latest_Matches.Latest_Match_Data import latest_match_data  # Import the DataFrame

    # Specify the absolute path to the database file
    db_file = "../../database/IPL_Prediction_Analysis.db"

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Create a cursor
    cursor = conn.cursor()

    # Define the table name
    table_name = 'Match_Data'

    # Check if the table already exists and create it if not
    cursor.execute(f'''
        SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'
    ''')
    existing_table = cursor.fetchone()

    if not existing_table:
        cursor.execute('''
            CREATE TABLE Match_Data (
                Match_ID INTEGER PRIMARY KEY,
                Innings TEXT,
                Venue TEXT,
                Date TEXT,
                Team1 TEXT,
                Team2 TEXT,
                Team1_runs INTEGER,
                Team1_wickets INTEGER,
                Team2_runs INTEGER,
                Team2_wickets INTEGER,
                Target INTEGER,
                Team1_played_Overs TEXT,
                Team2_played_Overs TEXT,
                Match_Result TEXT
            )
        ''')
        print("Table 'Match_Data' created successfully.")
        conn.commit()

    all_matches_data = latest_match_data()
    # Iterate over each row in the DataFrame
    for index, row in all_matches_data.iterrows():
        # Check if the row already exists in the database
        cursor.execute('''
            SELECT * FROM Match_Data 
            WHERE Innings = ? AND Venue = ? AND Date = ? AND Team1 = ? AND Team2 = ?
        ''', (row['Innings'], row['Venue'], row['Date'], row['Team1'], row['Team2']))

        existing_row = cursor.fetchone()

        # If the row exists, update it
        if existing_row:
            cursor.execute('''
                UPDATE Match_Data 
                SET Team1_runs = ?, Team1_wickets = ?, Team2_runs = ?, Team2_wickets = ?, Target = ?, Team1_played_Overs = ?, Team2_played_Overs = ?, Match_Result = ?
                WHERE Match_ID = ?
            ''', (row['Team1_runs'], row['Team1_wickets'], row['Team2_runs'], row['Team2_wickets'], row['Target'],
                  row['Team1_played_Overs'], row['Team2_played_Overs'], row['Match_Result'], existing_row[0]))
            print(f"Values updated for match: {row['Innings']} {row['Venue']} {row['Date']} {row['Team1']} {row['Team2']}")
        else:
            # If the row does not exist, insert it
            cursor.execute('''
                INSERT INTO Match_Data (Innings, Venue, Date, Team1, Team2, Team1_runs, Team1_wickets, Team2_runs, Team2_wickets, Target, Team1_played_Overs, Team2_played_Overs, Match_Result)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row['Innings'], row['Venue'], row['Date'], row['Team1'], row['Team2'], row['Team1_runs'],
                  row['Team1_wickets'], row['Team2_runs'], row['Team2_wickets'], row['Target'], row['Team1_played_Overs'],
                  row['Team2_played_Overs'], row['Match_Result']))
            print(f"Values inserted for match: {row['Innings']} {row['Venue']} {row['Date']} {row['Team1']} {row['Team2']}")

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

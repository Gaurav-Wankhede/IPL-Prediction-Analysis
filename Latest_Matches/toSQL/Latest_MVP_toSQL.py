def latest_mvp_sql():
    import sqlite3
    from Latest_Matches.Latest_MVP_Data import latest_mvp_data  # Import the DataFrame

    # Specify the absolute path to the database file
    db_file = "../../database/IPL_Prediction_Analysis.db"

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Create a cursor
    cursor = conn.cursor()

    # Define the table name
    table_name = 'MVP_Data'

    # Check if the table already exists and create it if not
    cursor.execute(f'''
        SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'
    ''')
    existing_table = cursor.fetchone()

    if not existing_table:
        cursor.execute('''
            CREATE TABLE MVP_Data (
                MVP_ID INTEGER PRIMARY KEY,
                Innings TEXT,
                Venue TEXT,
                Date TEXT,
                Player_Name TEXT,
                Team TEXT,
                Total_Impact INTEGER,
                Runs INTEGER,
                Balls_Faced INTEGER,
                Impact_Runs INTEGER,
                Batting_Impact INTEGER,
                Wickets INTEGER,
                Runs_Conceded INTEGER,
                Impact_Wickets INTEGER,
                Bowling_Impact INTEGER
            )
        ''')
        print("Table 'MVP_Data' created successfully.")
        conn.commit()

    final_data = latest_mvp_data()

    # Iterate through the rows of the final_data DataFrame and insert or update records in the database
    for index, row in final_data.iterrows():
        # Check if the row already exists in the database
        cursor.execute('''
            SELECT * FROM MVP_Data 
            WHERE MVP_ID = ? AND Innings = ? AND Venue = ? AND Date = ? AND Player_Name = ? AND Team = ?
        ''', (row["MVP_ID"], row["Innings"], row["Venue"], row["Date"], row["Player_Name"], row["Team"]))
        existing_row = cursor.fetchone()

        # If the row exists, update it
        if existing_row:
            cursor.execute('''
                UPDATE MVP_Data 
                SET Total_Impact = ?,
                    Runs = ?,
                    Balls_Faced = ?,
                    Impact_Runs = ?,
                    Batting_Impact = ?,
                    Wickets = ?,
                    Runs_Conceded = ?,
                    Impact_Wickets = ?,
                    Bowling_Impact = ?
                WHERE MVP_ID = ? AND Innings = ? AND Venue = ? AND Date = ? AND Player_Name = ? AND Team = ?
            ''', (row["Total_Impact"], row["Runs"], row["Balls_Faced"], row["Impact_Runs"], row["Batting_Impact"],
                  row["Wickets"], row["Runs_Conceded"], row["Impact_Wickets"], row["Bowling_Impact"],
                  row["MVP_ID"], row["Innings"], row["Venue"], row["Date"], row["Player_Name"], row["Team"]))
        else:
            # If the row does not exist, insert it
            cursor.execute('''
                INSERT INTO MVP_Data (MVP_ID, Innings, Venue, Date, Player_Name, Team, Total_Impact, Runs, Balls_Faced, Impact_Runs, Batting_Impact, Wickets, Runs_Conceded, Impact_Wickets, Bowling_Impact)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row["MVP_ID"], row["Innings"], row["Venue"], row["Date"], row["Player_Name"], row["Team"],
                  row["Total_Impact"], row["Runs"], row["Balls_Faced"], row["Impact_Runs"], row["Batting_Impact"],
                  row["Wickets"], row["Runs_Conceded"], row["Impact_Wickets"], row["Bowling_Impact"]))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

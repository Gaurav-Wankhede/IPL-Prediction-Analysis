def latest_batting_sql():
    import sqlite3
    from Latest_Matches.Latest_Batting import latest_batting # Import Batting.py and get access to combine_table

    # Specify the absolute path to the database file
    db_file = "../../database/IPL_Prediction_Analysis.db"

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Create a cursor
    cursor = conn.cursor()

    # Define the table name
    table_name = 'Batting'  # Change table name to 'Batting'

    # Check if the table already exists and create it if not
    cursor.execute(f'''
        SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'
    ''')
    existing_table = cursor.fetchone()

    if not existing_table:
        cursor.execute('''
            CREATE TABLE Batting (
                Batting_ID INTEGER PRIMARY KEY,
                Innings TEXT,
                Venue TEXT,
                Team TEXT,
                Date TEXT,
                Player_name TEXT,
                Dismissal_type TEXT,
                Runs TEXT,
                Balls TEXT,
                Dot_Balls TEXT,
                Strike_Rate TEXT,
                Fours TEXT,
                Sixes TEXT
            )
        ''')
        print(f"Table '{table_name}' created successfully.")

    # Commit the transaction
    conn.commit()

    combine_table = latest_batting()

    # Loop through combine_table and insert/update records
    for player_data in combine_table.itertuples():
        try:
            innings = player_data[1]  # Accessing the first column
            venue = player_data[2]  # Accessing the second column
            team = player_data[3]  # Accessing the third column
            date = player_data[4]  # Accessing the fourth column
            player_name = player_data[5]  # Accessing the fifth column
            dismissal_type = player_data[6]  # Accessing the sixth column
            r = player_data[7]  # Accessing the seventh column
            b = player_data[8]  # Accessing the eighth column
            m = player_data[9] if player_data[9] else "0"  # Accessing the ninth column, handle empty string case
            sr = player_data[10]  # Accessing the tenth column
            fours = player_data[11]  # Accessing the eleventh column
            sixes = player_data[12]  # Accessing the twelfth column

            # Check if the player data already exists in the database
            cursor.execute('''
                SELECT * FROM Batting 
                WHERE Innings = ? AND Venue = ? AND Team = ? AND Date = ? AND Player_name = ?
            ''', (innings, venue, team, date, player_name))

            existing_player = cursor.fetchone()

            # If the player data already exists, update it
            if existing_player:
                cursor.execute('''
                    UPDATE Batting
                    SET Dismissal_type = ?, Runs = ?, Balls = ?, Dot_Balls = ?, Strike_Rate = ?, Fours = ?, Sixes = ?
                    WHERE Batting_ID = ? AND Innings = ? AND Venue = ? AND Team = ? AND Date = ? AND Player_name = ?
                ''', (dismissal_type, r, b, m, sr, fours, sixes, existing_player[0], innings, venue, team, date, player_name))

                # Commit the transaction
                conn.commit()

                # Print a success message
                print(f"Values updated for player {player_name}.")
            else:
                # If the player data does not exist, insert it into the database
                cursor.execute('''
                    INSERT INTO Batting (Innings, Venue, Team, Date, Player_name, Dismissal_type, Runs, Balls, Dot_Balls, Strike_Rate, Fours, Sixes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (innings, venue, team, date, player_name, dismissal_type, r, b, m, sr, fours, sixes))

                # Commit the transaction
                conn.commit()

                # Print a success message
                print(f"Values inserted for player {player_name}.")

        except Exception as e:
            print(f"Error inserting data for player: {e}")

    # Close the connection
    conn.close()

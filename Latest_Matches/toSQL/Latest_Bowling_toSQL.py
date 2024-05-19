def latest_bowling_sql():
    import sqlite3
    from Latest_Matches.Latest_Bowling import latest_bowling

    # Specify the absolute path to the database file
    db_file = "../../database/IPL_Prediction_Analysis.db"

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Create a cursor
    cursor = conn.cursor()

    # Define the table name
    table_name = 'Bowling'

    # Check if the table already exists and create it if not
    cursor.execute(f'''
        SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'
    ''')
    existing_table = cursor.fetchone()

    if not existing_table:
        cursor.execute('''
            CREATE TABLE Bowling (
        Bowling_ID INTEGER PRIMARY KEY,
        Innings TEXT,
        Venue TEXT,
        Team TEXT,
        Date TEXT,
        Player_name TEXT,
        Overs TEXT,
        Maidens TEXT,
        Runs TEXT,
        Wickets TEXT,
        Economy_rate TEXT,
        Dot_ball TEXT,
        Fours TEXT,
        Sixes TEXT,
        Wides TEXT,
        No_balls TEXT
    )
        ''')
        print(f"Table '{table_name}' created successfully.")

    # Commit the transaction
    conn.commit()

    combine_table = latest_bowling()
    for player_data in combine_table.itertuples():
        try:
            innings = player_data[1]  # Accessing the first column
            venue = player_data[2]  # Accessing the second column
            team = player_data[3]  # Accessing the third column
            date = player_data[4]  # Accessing the fourth column
            player_name = player_data[5]  # Accessing the fifth column
            overs = player_data[6]  # Accessing the sixth column
            maidens = player_data[7]  # Accessing the seventh column
            runs = player_data[8]  # Accessing the eighth column
            wickets = player_data[9]  # Accessing the ninth column
            economy_rate = player_data[10]  # Accessing the tenth column
            dot_ball = player_data[11]  # Accessing the eleventh column
            fours = player_data[12]  # Accessing the twelfth column
            sixes = player_data[13]  # Accessing the thirteenth column
            wides = player_data[14]  # Accessing the fourteenth column
            no_balls = player_data[15]  # Accessing the fifteenth column

            # Check if the player data already exists in the database
            cursor.execute('''
                SELECT Bowling_ID FROM Bowling 
                WHERE Innings = ? AND Venue = ? AND Team = ? AND Date = ? AND Player_name = ?
            ''', (innings, venue, team, date, player_name))

            existing_player = cursor.fetchone()

            # If the player data exists, update it in the database
            if existing_player:
                cursor.execute('''
                    UPDATE Bowling 
                    SET Overs = ?, Maidens = ?, Runs = ?, Wickets = ?, Economy_rate = ?, Dot_ball = ?, Fours = ?, Sixes = ?, Wides = ?, No_balls = ?
                    WHERE Bowling_ID = ? AND Innings = ? AND Venue = ? AND Team = ? AND Date = ? AND Player_name = ?
                ''', (overs, maidens, runs, wickets, economy_rate, dot_ball, fours, sixes, wides, no_balls,
                      existing_player[0], innings, venue, team, date, player_name))

                # Commit the transaction
                conn.commit()

                # Print a success message
                print(f"Values updated for player {player_name}.")
            else:
                # If the player data does not exist, insert it into the database
                cursor.execute('''
                    INSERT INTO Bowling (Innings, Venue, Team, Date, Player_name, Overs, Maidens, Runs, Wickets, Economy_rate, Dot_ball, Fours, Sixes, Wides, No_balls)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (innings, venue, team, date, player_name, overs, maidens, runs, wickets,
                      economy_rate, dot_ball, fours, sixes, wides, no_balls))

                # Commit the transaction
                conn.commit()

                # Print a success message
                print(f"Values inserted for player {player_name}.")

        except Exception as e:
            print(f"Error inserting/updating data for player: {e}")

    # Close the connection
    conn.close()

import sqlite3
import os
from Prev_Matches.Match_data import match_data

class MatchDataSQLProcessor:
    @staticmethod
    def create_match_data_table(conn):
        try:
            cursor = conn.cursor()
            table_name = 'Match_Data'
            cursor.execute(f'''
                SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'
            ''')
            existing_table = cursor.fetchone()
            if existing_table:
                print(f"Table '{table_name}' already exists.")
            else:
                cursor.execute('''
                    CREATE TABLE Match_Data (
                        Match_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Innings TEXT,
                        Venue TEXT,
                        Start_Date TEXT,
                        End_Date TEXT,
                        Team1 TEXT,
                        Team2 TEXT,
                        Team1_runs INTEGER,
                        Team1_wickets INTEGER,
                        Team2_runs INTEGER,
                        Team2_wickets INTEGER,
                        Target INTEGER,
                        Team1_played_Overs TEXT,
                        Team2_played_Overs TEXT,
                        Team1_Max_Overs INTEGER,  -- Add Team1_Max_Overs column
                        Team2_Max_Overs INTEGER,  -- Add Team2_Max_Overs column
                        Match_Result TEXT
                    )
                ''')
                print(f"Table '{table_name}' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating or checking Match_Data table: {e}")

    @staticmethod
    def process_match_data(conn, match_data):
        if not conn:
            print("No database connection.")
            return
        # Fetch match data
        df = match_data()
        try:
            cursor = conn.cursor()

            # Loop through the DataFrame and insert/update records
            for index, row in df.iterrows():
                try:
                    # Extract data from the DataFrame row
                    match_data_list = row.tolist()
                    print(match_data_list)

                    # Exclude Match_ID field from match_data_list
                    match_data_values = match_data_list[:]

                    # Check if the row already exists in the database
                    cursor.execute('''
                        SELECT Match_ID FROM Match_Data 
                        WHERE Innings = ? AND Venue = ? AND Start_Date = ? AND End_Date = ? AND Team1 = ? AND Team2 = ?
                    ''', match_data_values[:6])

                    existing_row = cursor.fetchone()

                    # If the row exists, update it in the database
                    if existing_row:
                        cursor.execute('''
                            UPDATE Match_Data 
                            SET Team1_runs = ?, Team1_wickets = ?, Team2_runs = ?, Team2_wickets = ?, Target = ?, Team1_played_Overs = ?, Team2_played_Overs = ?, Team1_Max_Overs = ?, Team2_Max_Overs = ?, Match_Result = ?
                            WHERE Match_ID = ?
                        ''', match_data_values[6:] + [existing_row[0]])
                        print(
                            f"Values updated for match: {match_data_values[0]} {match_data_values[1]} {match_data_values[2]} {match_data_values[3]} {match_data_values[4]}")
                    else:
                        # If the row does not exist, insert it into the database
                        cursor.execute('''
                            INSERT INTO Match_Data (Innings, Venue, Start_Date, End_Date, Team1, Team2, Team1_runs, Team1_wickets, Team2_runs, Team2_wickets, Target, Team1_played_Overs, Team2_played_Overs, Team1_Max_Overs, Team2_Max_Overs, Match_Result)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', match_data_values)
                        print(
                            f"Values inserted for match: {match_data_values[0]} {match_data_values[1]} {match_data_values[2]} {match_data_values[3]} {match_data_values[4]}")

                    # Commit the transaction
                    conn.commit()

                except Exception as e:
                    print(f"Error inserting/updating data for match: {e}")

        except sqlite3.Error as e:
            print(f"Error processing match data: {e}")

    @classmethod
    def run(cls):
        global conn
        try:
            # Get the directory of the current script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Specify the relative path to the database file
            db_file = os.path.join(script_dir, "../../database/IPL_Prediction_Analysis.db")

            print(f"Database file: {db_file}")

            # Connect to the SQLite database
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()

            cls.create_match_data_table(conn)
            cls.process_match_data(conn, match_data)  # Pass match_data function as an argument

        except Exception as e:
            print(f"Error running MatchDataSQLProcessor: {e}")

        finally:
            if conn:
                conn.close()

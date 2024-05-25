import os
import sqlite3
from Latest_Matches.Latest_Match_Data import latest_match_data

class LatestMatchDataSQLProcessor:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.relative_db_path = os.path.normpath(
            os.path.join(self.script_dir, "../../database/IPL_Prediction_Analysis.db"))

        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.relative_db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        self.cursor = self.conn.cursor()

    def insert_or_update_data(self, data):
        all_matches_data = data

        # Define Match_ID column as INTEGER PRIMARY KEY AUTOINCREMENT
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Match_Data (
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
                Team1_played_Overs FLOAT,
                Team2_played_Overs FLOAT,
                Match_Result TEXT
            )
        ''')

        # Iterate over each row in the DataFrame
        for index, row in all_matches_data.iterrows():
            try:
                # Insert the row into the database, or update it if it already exists
                self.cursor.execute('''
                        INSERT INTO Match_Data (Innings, Venue, Start_Date, End_Date, Team1, Team2, Team1_runs, Team1_wickets, Team2_runs, Team2_wickets, Target, Team1_played_Overs, Team2_played_Overs, Match_Result)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(Match_ID) DO UPDATE SET
                            Innings = EXCLUDED.Innings,
                            Venue = EXCLUDED.Venue,
                            Start_Date = EXCLUDED.Start_Date,
                            End_Date = EXCLUDED.End_Date,
                            Team1 = EXCLUDED.Team1,
                            Team2 = EXCLUDED.Team2,
                            Team1_runs = EXCLUDED.Team1_runs,
                            Team1_wickets = EXCLUDED.Team1_wickets,
                            Team2_runs = EXCLUDED.Team2_runs,
                            Team2_wickets = EXCLUDED.Team2_wickets,
                            Target = EXCLUDED.Target,
                            Team1_played_Overs = EXCLUDED.Team1_played_Overs,
                            Team2_played_Overs = EXCLUDED.Team2_played_Overs,
                            Match_Result = EXCLUDED.Match_Result
                    ''', (
                    row['Innings'], row['Venue'], row['Start_Date'], row['End_Date'], row['Team1'], row['Team2'],
                    row['Team1_runs'],
                    row['Team1_wickets'], row['Team2_runs'], row['Team2_wickets'], row['Target'],
                    row['Team1_played_Overs'],
                    row['Team2_played_Overs'], row['Match_Result']))


                print(
                f"Values inserted/updated for match: {row['Innings']} {row['Venue']} {row['Start_Date']} {row['End_Date']} {row['Team1']} {row['Team2']}"
                )
            except Exception as e:
                print(f"Error inserting/updating data for match: {e}")

        # Commit the transaction
        self.conn.commit()

    def run(self):
        self.connect()
        all_matches_data = latest_match_data()
        self.insert_or_update_data(all_matches_data)
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()

import os
import sqlite3
from Latest_Matches.Latest_MVP_Data import latest_mvp_data

class LatestMVPDataSQLProcessor:
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
        final_data = data

        # Define MVP_ID column as INTEGER PRIMARY KEY AUTOINCREMENT
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS MVP_Data (
                MVP_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Innings TEXT,
                Venue TEXT,
                Start_Date TEXT,
                End_Date TEXT,
                Player_Name TEXT,
                Team TEXT,
                Total_Impact REAL,
                Runs INTEGER,
                Balls_Faced INTEGER,
                Impact_Runs REAL,
                Batting_Impact REAL,
                Wickets INTEGER,
                Runs_Conceded INTEGER,
                Impact_Wickets REAL,
                Bowling_Impact REAL
            )
        ''')

        # Iterate through the rows of the final_data DataFrame and insert or update records in the database
        for index, row in final_data.iterrows():
            try:
                # Insert the record into the database
                self.cursor.execute('''
                    INSERT INTO MVP_Data (Innings, Venue, Start_Date, End_Date, Player_Name, Team, Total_Impact, Runs, Balls_Faced, Impact_Runs, Batting_Impact, Wickets, Runs_Conceded, Impact_Wickets, Bowling_Impact)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (row["Innings"], row["Venue"], row["Start_Date"], row["End_Date"], row["Player_Name"], row["Team"],
                      row["Total_Impact"], row["Runs"], row["Balls_Faced"], row["Impact_Runs"], row["Batting_Impact"],
                      row["Wickets"], row["Runs_Conceded"], row["Impact_Wickets"], row["Bowling_Impact"]))

                print(f"Values inserted for MVP: {row['Player_Name']}")

            except sqlite3.IntegrityError as e:
                # If the record already exists, update it
                if "UNIQUE constraint failed" in str(e):
                    self.cursor.execute('''
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
                        WHERE MVP_ID = ?
                    ''', (
                    row["Total_Impact"], row["Runs"], row["Balls_Faced"], row["Impact_Runs"], row["Batting_Impact"],
                    row["Wickets"], row["Runs_Conceded"], row["Impact_Wickets"], row["Bowling_Impact"], row["MVP_ID"]))

                    print(f"Values updated for MVP: {row['Player_Name']}")

                else:
                    print(f"Error inserting/updating data for MVP: {e}")

        # Commit the changes to the database
        self.conn.commit()

    def run(self):
        self.connect()
        final_data = latest_mvp_data()
        self.insert_or_update_data(final_data)
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()

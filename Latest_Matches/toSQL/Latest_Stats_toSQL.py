import os
import sqlite3
from Latest_Matches.Latest_Stats import latest_stats


class LatestStatsDataSQLProcessor:
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
        df = data

        # Define Stats_ID column as INTEGER PRIMARY KEY AUTOINCREMENT
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Stats_Data (
                Stats_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Innings TEXT,
                Venue TEXT,
                Start_Date TEXT,
                End_Date TEXT,
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

        # Iterate through the rows of the DataFrame and insert or update records in the database
        for index, row in df.iterrows():
            try:
                # Check if the record with the given Stats_ID already exists
                self.cursor.execute('''
                    SELECT * FROM Stats_Data WHERE
                        Innings = ? AND
                        Venue = ? AND
                        Start_Date = ? AND
                        End_Date = ? AND
                        Team = ? AND
                        Player1 = ? AND
                        Player2 = ? AND
                        Player1_Runs = ? AND
                        Player1_Balls = ? AND
                        Partnership_Runs = ? AND
                        Partnership_Balls = ? AND
                        Player2_Runs = ? AND
                        Player2_Balls = ?
                ''', (
                    row['Innings'], row['Venue'], row['Start_Date'], row['End_Date'], row['Team'],
                    row['Player1'], row['Player2'], row['Player1_Runs'], row['Player1_Balls'],
                    row['Partnership_Runs'], row['Partnership_Balls'], row['Player2_Runs'], row['Player2_Balls']
                ))

                result = self.cursor.fetchone()

                if result is not None:
                    # Update the existing record
                    self.cursor.execute('''
                        UPDATE Stats_Data
                        SET
                            Innings = ?,
                            Venue = ?,
                            Start_Date = ?,
                            End_Date = ?,
                            Team = ?,
                            Player1 = ?,
                            Player2 = ?,
                            Player1_Runs = ?,
                            Player1_Balls = ?,
                            Partnership_Runs = ?,
                            Partnership_Balls = ?,
                            Player2_Runs = ?,
                            Player2_Balls = ?
                        WHERE
                            Stats_ID = ?
                    ''', (row['Innings'], row['Venue'], row['Start_Date'], row['End_Date'], row['Team'], row['Player1'],
                          row['Player2'], row['Player1_Runs'], row['Player1_Balls'], row['Partnership_Runs'],
                          row['Partnership_Balls'], row['Player2_Runs'], row['Player2_Balls']))

                else:
                    # Insert a new record with the next available Stats_ID
                    self.cursor.execute('''
                        INSERT INTO Stats_Data
                            (Innings, Venue, Start_Date, End_Date, Team, Player1, Player2, Player1_Runs, Player1_Balls, Partnership_Runs, Partnership_Balls, Player2_Runs, Player2_Balls)
                        VALUES
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (row['Innings'], row['Venue'], row['Start_Date'], row['End_Date'], row['Team'],
                          row['Player1'],
                          row['Player2'], row['Player1_Runs'], row['Player1_Balls'], row['Partnership_Runs'],
                          row['Partnership_Balls'], row['Player2_Runs'], row['Player2_Balls']))

            except Exception as e:
                print(f"Error inserting/updating data for stats: {e}")

        # Commit the transaction
        self.conn.commit()

    def run(self):
        self.connect()
        df = latest_stats()
        self.insert_or_update_data(df)
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()

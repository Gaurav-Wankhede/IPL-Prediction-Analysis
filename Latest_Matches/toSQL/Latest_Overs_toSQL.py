import os
import sqlite3
from Latest_Matches.Latest_Overs import latest_overs


class LatestOversDataSQLProcessor:
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

        # Define Overs_ID column as INTEGER PRIMARY KEY AUTOINCREMENT
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Overs_Data (
                Overs_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Innings TEXT,
                Venue TEXT,
                Start_Date TEXT,
                End_Date TEXT,
                Team_Name TEXT,
                Overs REAL,
                Team_Runs INTEGER,
                Team_Wickets INTEGER,
                Team_Total_Runs INTEGER,
                Team_Total_Wickets INTEGER
            )
        ''')

        # Iterate through the rows of the DataFrame and insert or update records in the database
        for index, row in df.iterrows():
            try:
                # Try to update the existing record
                self.cursor.execute('''
                    UPDATE Overs_Data
                    SET
                        Overs = ?,
                        Team_Runs = ?,
                        Team_Wickets = ?,
                        Team_Total_Runs = ?,
                        Team_Total_Wickets = ?
                    WHERE
                        Innings = ? AND Venue = ? AND Start_Date = ? AND End_Date = ? AND Team_Name = ? AND Overs = ?
                ''', (
                    row['Overs'], row['Team_Runs'], row['Team_Wickets'], row['Team_Total_Runs'],
                    row['Team_Total_Wickets'],
                    row['Innings'], row['Venue'], row['Start_Date'], row['End_Date'], row['Team_Name'], row['Overs']))

                # If no rows were updated, perform an insertion
                if self.cursor.rowcount == 0:
                    self.cursor.execute('''
                        INSERT INTO Overs_Data
                            (Innings, Venue, Start_Date, End_Date, Team_Name, Overs, Team_Runs, Team_Wickets, Team_Total_Runs, Team_Total_Wickets)
                        VALUES
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row['Innings'], row['Venue'], row['Start_Date'], row['End_Date'], row['Team_Name'],
                        row['Overs'],
                        row['Team_Runs'],
                        row['Team_Wickets'], row['Team_Total_Runs'], row['Team_Total_Wickets']))


            except Exception as e:
                print(f"Error inserting/updating data for overs: {e}")

        # Commit the transaction
        self.conn.commit()

    def run(self):
        self.connect()
        df = latest_overs()
        self.insert_or_update_data(df)
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()

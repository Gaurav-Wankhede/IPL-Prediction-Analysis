import sqlite3
import os
from Prev_Matches.Batting import batting

class BattingSQLProcessor:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.relative_db_path = os.path.normpath(os.path.join(self.script_dir, "../../database/IPL_Prediction_Analysis.db"))

    def connect_to_database(self):
        if not os.path.exists(self.relative_db_path):
            print(f"Database file does not exist: {self.relative_db_path}")
            return None

        conn = sqlite3.connect(self.relative_db_path)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        return conn

    def create_batting_table(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Batting'")
            table_exists = cursor.fetchone()
            if table_exists:
                print("Batting table already exists.")
            else:
                cursor.execute('''
                    CREATE TABLE Batting (
                        Batting_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Innings TEXT,
                        Venue TEXT,
                        Team TEXT,
                        Start_Date TEXT,
                        End_Date TEXT,
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
                print("Batting table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating or checking batting table: {e}")

    def process_batting_data(self, conn):
        if not conn:
            print("No database connection.")
            return

        combine_table = batting()

        try:
            with conn:
                cursor = conn.cursor()
                for row in combine_table.itertuples(index=False, name=None):
                    cursor.execute('''
                        SELECT 1 FROM Batting 
                        WHERE Innings = ? AND Venue = ? AND Team = ? AND Start_Date = ? AND End_Date = ? AND Player_name = ?
                        LIMIT 1
                    ''', (row[0], row[1], row[2], row[3], row[4], row[5]))
                    existing_row = cursor.fetchone()
                    if not existing_row:
                        # Row does not exist, insert new data
                        conn.execute('''
                            INSERT INTO Batting (Innings, Venue, Team, Start_Date, End_Date, Player_name, Dismissal_type, Runs, Balls, Dot_Balls, Strike_Rate, Fours, Sixes)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', row[1:])  # Omitting the first element (Batting_ID) from the tuple

                    else:
                        print("Skipping duplicate row:", row)
            print("Values inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def run(self):
        try:
            conn = self.connect_to_database()
            if conn:
                self.create_batting_table(conn)
                self.process_batting_data(conn)
        finally:
            if conn:
                conn.close()

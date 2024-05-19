import sqlite3
import os
from Prev_Matches.MVP_Data import mvp_data

class MVPDataSQLProcessor:
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

    def create_mvp_table(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MVP_Data'")
            table_exists = cursor.fetchone()
            if table_exists:
                print("MVP_Data table already exists.")
            else:
                cursor.execute('''
                    CREATE TABLE MVP_Data (
                        MVP_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Innings TEXT,
                        Venue TEXT,
                        Start_Date TEXT,
                        End_Date TEXT,
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
                print("MVP_Data table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating or checking MVP_Data table: {e}")

    def process_mvp_data(self, conn):
        if not conn:
            print("No database connection.")
            return

        final_data = mvp_data()

        try:
            with conn:
                cursor = conn.cursor()
                for row in final_data.itertuples(index=False):
                    cursor.execute('''
                        SELECT MVP_ID FROM MVP_Data 
                        WHERE Innings = ? AND Venue = ? AND Start_Date = ? AND End_Date = ? AND Player_Name = ? AND Team = ?
                    ''', (row.Innings, row.Venue, row.Start_Date, row.End_Date, row.Player_Name, row.Team))

                    existing_row = cursor.fetchone()
                    if existing_row:
                        # Row exists, update it
                        cursor.execute('''
                            UPDATE MVP_Data 
                            SET Total_Impact = ?, Runs = ?, Balls_Faced = ?, Impact_Runs = ?, Batting_Impact = ?, Wickets = ?, Runs_Conceded = ?, Impact_Wickets = ?, Bowling_Impact = ?
                            WHERE MVP_ID = ?
                        ''', (row.Total_Impact, row.Runs, row.Balls_Faced, row.Impact_Runs, row.Batting_Impact,
                              row.Wickets, row.Runs_Conceded, row.Impact_Wickets, row.Bowling_Impact,
                              existing_row[0]))
                        print(f"Values updated for MVP: {row.Player_Name}")

                    else:
                        # Row does not exist, insert new data
                        cursor.execute('''
                            INSERT INTO MVP_Data (Innings, Venue, Start_Date, End_Date, Player_Name, Team, Total_Impact, Runs, Balls_Faced, Impact_Runs, Batting_Impact, Wickets, Runs_Conceded, Impact_Wickets, Bowling_Impact)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (row.Innings, row.Venue, row.Start_Date, row.End_Date, row.Player_Name, row.Team,
                              row.Total_Impact, row.Runs, row.Balls_Faced, row.Impact_Runs, row.Batting_Impact,
                              row.Wickets, row.Runs_Conceded, row.Impact_Wickets, row.Bowling_Impact))
                        print(f"Values inserted for MVP: {row.Player_Name}")

            print("Data processing completed.")
        except sqlite3.Error as e:
            print(f"Error processing MVP data: {e}")

    def run(self):
        global conn
        try:
            conn = self.connect_to_database()
            if conn:
                self.create_mvp_table(conn)
                self.process_mvp_data(conn)
        finally:
            if conn:
                conn.close()

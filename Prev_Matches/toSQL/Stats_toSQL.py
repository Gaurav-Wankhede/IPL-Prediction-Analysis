import sqlite3
import os
from Prev_Matches.Stats import stats

class StatsSQLProcessor:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_file = os.path.normpath(
            os.path.join(self.script_dir, "../../database/IPL_Prediction_Analysis.db"))
        self.table_name = 'Stats_Data'

    def connect(self):
        if not os.path.exists(self.db_file):
            print(f"Database file does not exist: {self.db_file}")
            return None
        conn = sqlite3.connect(self.db_file)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        return conn

    def create_table(self, conn):
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'
        ''')
        table_exists = cursor.fetchone()

        if table_exists:
            print(f"Table '{self.table_name}' already exists.")
        else:
            cursor.execute(f'''
                CREATE TABLE {self.table_name} (
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
            print(f"Table '{self.table_name}' created successfully.")
        cursor.close()

    def insert_or_update_data(self, conn, df):
        cursor = conn.cursor()
        try:
            for row in df.itertuples(index=False, name=None):
                # Check if the row already exists in the database
                cursor.execute(f'''
                    SELECT 1 FROM {self.table_name}
                    WHERE Innings = ? AND Venue = ? AND Start_Date = ? AND End_Date = ? AND Team = ? AND Player1 = ? AND Player2 = ?
                ''', row[:7])

                existing_row = cursor.fetchone()
                print("Row being processed:")
                print(row)

                if not existing_row:
                    # Row does not exist, insert new data
                    cursor.execute(f'''
                        INSERT INTO {self.table_name} (Innings, Venue, Start_Date, End_Date, Team, Player1, Player2, Player1_Runs, Player1_Balls, Partnership_Runs, Partnership_Balls, Player2_Runs, Player2_Balls)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', row)
                    print("Inserted row:", row)
                else:
                    print("Skipping duplicate row:", row)

                conn.commit()
            print("Data inserted/updated successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting/updating data for stats: {e}")
        finally:
            cursor.close()

    def run(self):
        conn = self.connect()
        if conn is None:
            return
        try:
            self.create_table(conn)
            df = stats()
            self.insert_or_update_data(conn, df)
        finally:
            if conn:
                conn.close()
                print("Database connection closed.")

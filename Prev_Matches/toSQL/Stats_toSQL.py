import sqlite3
import os
from Prev_Matches.Stats import stats

class StatsSQLProcessor:
    def __init__(self):
        self.db_file = "../../database/IPL_Prediction_Analysis.db"
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def create_table(self):
        table_name = 'Stats_Data'
        self.cursor.execute(f'''
            SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'
        ''')
        table_exists = self.cursor.fetchone()

        if table_exists:
            print(f"Table '{table_name}' already exists.")
        else:
            self.cursor.execute('''
                CREATE TABLE Stats_Data (
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

            print(f"Table '{table_name}' created successfully.")

    def insert_or_update_data(self, df):
        try:
            for row in df.itertuples(index=False, name=None):
                # Check if the row already exists in the database
                self.cursor.execute('''
                    SELECT 1 FROM Stats_Data 
                    WHERE Innings = ? AND Venue = ? AND Start_Date = ? AND End_Date = ? AND Team = ? AND Player1 = ? AND Player2 = ?
                ''', row[:7])

                existing_row = self.cursor.fetchone()
                print("Row being inserted:")
                print(row)
                if not existing_row:
                    # Row does not exist, insert new data
                    self.cursor.execute('''
                        INSERT INTO Stats_Data (Innings, Venue, Start_Date, End_Date, Team, Player1, Player2, Player1_Runs, Player1_Balls, Partnership_Runs, Partnership_Balls, Player2_Runs, Player2_Balls)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', row)

                else:
                    print("Skipping duplicate row:", row)
                self.conn.commit()
            print("Data inserted/updated successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting/updating data for stats: {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def run(self):
        self.connect()
        self.create_table()
        df = stats()
        self.insert_or_update_data(df)
        self.close_connection()

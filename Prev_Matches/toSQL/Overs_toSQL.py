import sqlite3
import os
from Prev_Matches.Overs import overs


class OversSQLProcessor:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.normpath(
            os.path.join(self.script_dir, "../../database/IPL_Prediction_Analysis.db"))
        self.table_name = 'Overs_Data'

    def connect_to_database(self):
        if not os.path.exists(self.db_path):
            print(f"Database file does not exist: {self.db_path}")
            return None

        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        return conn

    def create_table_if_not_exists(self, conn):
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'
        ''')
        existing_table = cursor.fetchone()

        if not existing_table:
            cursor.execute(f'''
                CREATE TABLE {self.table_name} (
                    Overs_ID INTEGER PRIMARY KEY,
                    Innings TEXT,
                    Venue TEXT,
                    Start_Date TEXT,
                    End_Date TEXT,
                    Team_Name TEXT,
                    Overs INTEGER,
                    Team_Runs INTEGER,
                    Team_Wickets INTEGER,
                    Team_Total_Runs INTEGER,
                    Team_Total_Wickets INTEGER
                )
            ''')
            print(f"Table '{self.table_name}' created successfully.")
        cursor.close()

    def process_overs_data(self):
        df = overs()

        with self.connect_to_database() as conn:
            if conn is None:
                return

            self.create_table_if_not_exists(conn)

            cursor = conn.cursor()
            for index, row in df.iterrows():
                try:
                    cursor.execute(f'''
                        SELECT * FROM {self.table_name}
                        WHERE Overs_ID = ? AND Innings = ? AND Venue = ? AND Start_Date = ? AND End_Date = ? AND Team_Name = ?
                    ''', (
                    row['Over_ID'], row['Innings'], row['Venue'], row['Start_Date'], row['End_Date'], row['Team_Name']))

                    existing_row = cursor.fetchone()

                    if existing_row:
                        cursor.execute(f'''
                            UPDATE {self.table_name}
                            SET
                                Overs = ?,
                                Team_Runs = ?,
                                Team_Wickets = ?,
                                Team_Total_Runs = ?,
                                Team_Total_Wickets = ?
                            WHERE 
                                Overs_ID = ? AND Innings = ? AND Venue = ? AND Start_Date = ? AND End_Date = ? AND Team_Name = ?
                        ''', (
                            row['Overs'], row['Team_Runs'], row['Team_Wickets'], row['Team_Total_Runs'],
                            row['Team_Total_Wickets'],
                            row['Over_ID'], row['Innings'], row['Venue'], row['Start_Date'], row['End_Date'],
                            row['Team_Name']))
                    else:
                        cursor.execute(f'''
                            INSERT INTO {self.table_name} 
                                (Overs_ID, Innings, Venue, Start_Date, End_Date, Team_Name, Overs, Team_Runs, Team_Wickets, Team_Total_Runs, Team_Total_Wickets)
                            VALUES
                                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            row['Over_ID'], row['Innings'], row['Venue'], row['Start_Date'], row['End_Date'],
                            row['Team_Name'],
                            row['Overs'], row['Team_Runs'], row['Team_Wickets'], row['Team_Total_Runs'],
                            row['Team_Total_Wickets']))

                    print(f"Data inserted/updated for overs: {row}")
                    conn.commit()

                except Exception as e:
                    print(f"Error inserting/updating data for overs: {e}")
            cursor.close()

    def run(self):
        self.process_overs_data()

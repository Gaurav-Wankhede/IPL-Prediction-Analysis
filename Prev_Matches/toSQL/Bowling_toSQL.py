import sqlite3
import os
from Prev_Matches.Bowling import bowling

class BowlingSQLProcessor:
    relative_db_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../database/IPL_Prediction_Analysis.db"))

    @classmethod
    def connect_to_database(cls):
        if not os.path.exists(cls.relative_db_path):
            print(f"Database file does not exist: {cls.relative_db_path}")
            return None

        conn = sqlite3.connect(cls.relative_db_path)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        return conn

    @classmethod
    def create_bowling_table(cls, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Bowling'")
            table_exists = cursor.fetchone()
            if table_exists:
                print("Bowling table already exists.")
            else:
                cursor.execute('''
                    CREATE TABLE Bowling (
                        Bowling_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Innings TEXT,
                        Venue TEXT,
                        Team TEXT,
                        Start_Date TEXT,
                        End_Date TEXT,
                        Bowling_Player TEXT,
                        Overs TEXT,
                        Maidens TEXT,
                        Runs TEXT,
                        Wickets TEXT,
                        Economy_rate TEXT,
                        Dot_ball TEXT,
                        Fours TEXT,
                        Sixes TEXT,
                        Wides TEXT,
                        No_balls TEXT
                    )
                ''')
                print("Bowling table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating or checking bowling table: {e}")

    @classmethod
    def process_bowling_data(cls, conn):
        if not conn:
            print("No database connection.")
            return

        combine_table = bowling()

        try:
            with conn:
                cursor = conn.cursor()
                for player_data in combine_table.itertuples():
                    cursor.execute('''
                        SELECT Bowling_ID FROM Bowling 
                        WHERE Innings = ? AND Venue = ? AND Team = ? AND Start_Date = ? AND End_Date = ? AND Bowling_Player = ?
                    ''', player_data[1:7])
                    existing_player = cursor.fetchone()
                    if existing_player:
                        cursor.execute('''
                            UPDATE Bowling 
                            SET Overs = ?, Maidens = ?, Runs = ?, Wickets = ?, Economy_rate = ?, Dot_ball = ?, Fours = ?, Sixes = ?, Wides = ?, No_balls = ?
                            WHERE Bowling_ID = ?
                        ''', player_data[8:] + (existing_player[0],))
                        print(f"Values updated for player {player_data.Bowling_Player}.")
                    else:
                        cursor.execute('''
                            INSERT INTO Bowling (Innings, Venue, Team, Start_Date, End_Date, Bowling_Player, Overs, Maidens, Runs, Wickets, Economy_rate, Dot_ball, Fours, Sixes, Wides, No_balls)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', player_data[1:])

                        print(f"Values inserted for player {player_data.Bowling_Player}.")
        except sqlite3.Error as e:
            print(f"Error inserting/updating data: {e}")
    @classmethod
    def run(cls):
        try:
            conn = cls.connect_to_database()
            if conn:
                cls.create_bowling_table(conn)
                cls.process_bowling_data(conn)
        finally:
            if conn:
                conn.close()

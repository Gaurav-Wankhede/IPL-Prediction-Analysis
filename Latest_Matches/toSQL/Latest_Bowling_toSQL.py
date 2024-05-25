import os
import sqlite3
from Latest_Matches.Latest_Bowling import latest_bowling


class LatestBowlingSQLProcessor:
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

    def insert_or_update_data(self, table_name, data):
        combine_table = data

        # Get the current maximum value of the Bowling_ID column
        self.cursor.execute('''
            SELECT MAX(Bowling_ID) FROM Bowling
        ''')
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            max_id = 0

        # Loop through combine_table and insert/update records
        for player_data in combine_table.itertuples():
            try:
                innings = player_data[1]
                venue = player_data[2]
                team = player_data[3]
                start_date = player_data[4]
                end_date = player_data[5]
                player_name = player_data[6]
                overs = player_data[7]
                maidens = player_data[8]
                runs = player_data[9]
                wickets = player_data[10]
                economy_rate = player_data[11]
                dot_ball = player_data[12]
                fours = player_data[13]
                sixes = player_data[14]
                wides = player_data[15]
                no_balls = player_data[16]


                # Check if the player data already exists in the database
                self.cursor.execute('''
                    SELECT * FROM Bowling
                    WHERE Innings = ? AND Venue = ? AND Team = ? AND Start_Date = ? AND End_Date = ? AND Bowling_Player = ?
                ''', (innings, venue, team, start_date, end_date, player_name))

                existing_player = self.cursor.fetchone()

                # If the player data exists, update it in the database
                if existing_player:
                    self.cursor.execute('''
                        UPDATE Bowling
                        SET Overs = ?, Maidens = ?, Runs = ?, Wickets = ?, Economy_rate = ?, Dot_ball = ?, Fours = ?, Sixes = ?, Wides = ?, No_balls = ?
                        WHERE Bowling_ID = ?
                    ''', (overs, maidens, runs, wickets, economy_rate, dot_ball, fours, sixes, wides, no_balls,
                          existing_player[0]))

                    # Commit the transaction
                    self.conn.commit()

                    # Print a success message
                    print(f"Values updated for player {player_name}.")
                else:
                    # If the player data does not exist, insert it into the database
                    # Increment the Bowling_ID value
                    new_id = max_id + 1

                    self.cursor.execute('''
                        INSERT INTO Bowling (Bowling_ID, Innings, Venue, Team, Start_Date, End_Date, Bowling_Player, Overs, Maidens, Runs, Wickets, Economy_rate, Dot_ball, Fours, Sixes, Wides, No_balls)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (new_id, innings, venue, team, start_date, end_date, player_name, overs, maidens, runs, wickets,
                          economy_rate, dot_ball, fours, sixes, wides, no_balls))

                    # Commit the transaction
                    self.conn.commit()

                    # Update the maximum value of the Bowling_ID column
                    max_id = new_id

                    # Print a success message
                    print(f"Values inserted for player {player_name}.")

            except Exception as e:
                print(f"Error inserting/updating data for player: {e}")

    def run(self):
        self.connect()
        combine_table = latest_bowling()
        self.insert_or_update_data('Bowling', combine_table)
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()

import os
import sqlite3
from Latest_Matches.Latest_Batting import latest_batting


class LatestBattingSQLProcessor:
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

    def get_max_id(self):
        self.cursor.execute('''
            SELECT MAX(Batting_ID) FROM Batting
        ''')
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            max_id = 0
        return max_id

    def insert_or_update_data(self, table_name, data):
        # Get the current maximum value of the Batting_ID column
        max_id = self.get_max_id()

        # Loop through combine_table and insert/update records
        global player_name
        for player_data in data.itertuples(index=False):
            try:
                innings = player_data[0]
                venue = player_data[1]
                team = player_data[2]
                start_date = player_data[3]
                end_date = player_data[4]
                player_name = player_data[5]
                dismissal_type = player_data[6]
                r = player_data[7]
                b = player_data[8]
                m = player_data[9]
                fours= player_data[10]
                sixes = player_data[11]
                sr = player_data[12]


                # Check if the player data already exists in the database
                self.cursor.execute('''SELECT Batting_ID FROM Batting WHERE Innings = ? AND Venue = ? AND Team = ? AND Start_date = ? AND End_date = ? AND Player_name = ?''',
                                    (innings, venue, team, start_date, end_date, player_name))


                existing_player = self.cursor.fetchone()

                # If the player data already exists, update it
                if existing_player:
                    self.cursor.execute(f'''
                        UPDATE {table_name}
                        SET Dismissal_type = ?, Runs = ?, Balls = ?, Dot_Balls = ?, Fours = ?, Sixes = ?, Strike_Rate = ?
                        WHERE Batting_ID = ?
                    ''', (dismissal_type, r, b, m, fours, sixes, sr, existing_player[0]))

                    # Commit the transaction
                    self.conn.commit()

                    # Print a success message
                    print(f"Values updated for player {player_name}.")
                else:
                    # If the player data does not exist, insert it into the database
                    # Increment the Batting_ID value
                    new_id = max_id + 1

                    self.cursor.execute(f'''
                        INSERT INTO {table_name} (Batting_ID, Innings, Venue, Team, Start_date, End_date, Player_name, Dismissal_type, Runs, Balls, Dot_Balls, Fours, Sixes, Strike_Rate)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (new_id, innings, venue, team, start_date, end_date, player_name, dismissal_type, r, b, m, fours, sixes, sr))

                    # Commit the transaction
                    self.conn.commit()

                    # Update the maximum value of the Batting_ID column
                    max_id = new_id

                    # Print a success message
                    print(f"Values inserted for player {player_name} with ID {new_id}.")

            except Exception as e:
                print(f"Error inserting data for player {player_name}: {e}")

    def run(self):
        self.connect()
        combine_table = latest_batting()
        self.insert_or_update_data('Batting', combine_table)
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()

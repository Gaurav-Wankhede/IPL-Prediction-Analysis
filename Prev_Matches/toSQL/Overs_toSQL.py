import sqlite3
from Prev_Matches.Overs import overs

class OversSQLProcessor:
    def __init__(self):
        self.db_file_path = "../../database/IPL_Prediction_Analysis.db"
        self.table_name = 'Overs_Data'

    def create_table_if_not_exists(self, cursor):
        cursor.execute(f'''
            SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'
        ''')
        existing_table = cursor.fetchone()

        if not existing_table:
            cursor.execute('''
                CREATE TABLE Overs_Data (
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

    def process_overs_data(self):
        df = overs()

        # Connect to the SQLite database using a context manager
        with sqlite3.connect(self.db_file_path) as conn:
            cursor = conn.cursor()

            # Create the table if it does not exist
            self.create_table_if_not_exists(cursor)

            for index, row in df.iterrows():
                try:
                    # Check if the row already exists in the database
                    cursor.execute('''
                        SELECT * FROM Overs_Data 
                        WHERE Overs_ID = ? AND Innings = ? AND Venue = ? AND Start_Date = ? AND End_Date = ? AND Team_Name = ?
                    ''', (row['Over_ID'], row['Innings'], row['Venue'], row['Start_Date'], row['End_Date'], row['Team_Name']))

                    existing_row = cursor.fetchone()

                    if existing_row:
                        # If the row exists, update it
                        cursor.execute('''
                            UPDATE Overs_Data 
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
                            row['Over_ID'], row['Innings'], row['Venue'], row['Start_Date'], row['End_Date'], row['Team_Name']))
                    else:
                        # If the row does not exist, insert it
                        cursor.execute('''
                            INSERT INTO Overs_Data 
                                (Overs_ID, Innings, Venue, Start_Date, End_Date, Team_Name, Overs, Team_Runs, Team_Wickets, Team_Total_Runs, Team_Total_Wickets)
                            VALUES
                                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            row['Over_ID'], row['Innings'], row['Venue'], row['Start_Date'], row['End_Date'], row['Team_Name'],
                            row['Overs'], row['Team_Runs'],
                            row['Team_Wickets'], row['Team_Total_Runs'], row['Team_Total_Wickets']))

                    print(f"Data inserted/updated for overs: {row}")
                    # Commit the transaction
                    conn.commit()

                except Exception as e:
                    print(f"Error inserting/updating data for overs: {e}")

    def run(self):
        self.process_overs_data()


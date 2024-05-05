import pyodbc
from Latest_Matches.Latest_Batting import combine_table  # Import Batting.py and get access to combine_table

# Define your SQL Server connection parameters
server = r'DESKTOP-F8QC9QH\SQLEXPRESS'
database = r'IPL_Prediction_Analysis'

# Define the table name
table_name = 'Batting'  # Change table name to 'Batting'

# Connect to the database
conn = pyodbc.connect(r'DRIVER={SQL Server};'
                      r'SERVER=DESKTOP-F8QC9QH\SQLEXPRESS;'
                      r'DATABASE=IPL_Prediction_Analysis;'
                      r'Trusted_Connection=yes;')

# Check if the table already exists and create it if not
cursor = conn.cursor()
if not cursor.tables(table=table_name, tableType='TABLE').fetchone():
    cursor.execute('''
        CREATE TABLE Batting (
            Batting_ID int IDENTITY(1,1) PRIMARY KEY,
            Innings nvarchar(255),
            Venue nvarchar(255),
            Team nvarchar(255),
            Date nvarchar(255),
            Player_name nvarchar(255),
            Dismissal_type nvarchar(255),
            Runs nvarchar(255),
            Balls nvarchar(255),
            Dot_Balls nvarchar(255),
            Strike_Rate nvarchar(255),
            Fours nvarchar(255),
            Sixes nvarchar(255)
        )
    ''')
    print(f"Table '{table_name}' created successfully.")

# Commit the transaction
conn.commit()

# Loop through combine_table and insert/update records
for player_data in combine_table.itertuples():
    try:
        innings = player_data[1]  # Accessing the first column
        venue = player_data[2]  # Accessing the second column
        team = player_data[3]  # Accessing the third column
        date = player_data[4]  # Accessing the fourth column
        player_name = player_data[5]  # Accessing the fifth column
        dismissal_type = player_data[6]  # Accessing the sixth column
        r = player_data[7]  # Accessing the seventh column
        b = player_data[8]  # Accessing the eighth column
        m = player_data[9] if player_data[9] else "0"  # Accessing the ninth column, handle empty string case
        sr = player_data[10]  # Accessing the tenth column
        fours = player_data[11]  # Accessing the eleventh column
        sixes = player_data[12]  # Accessing the twelfth column

        # Check if the player data already exists in the database
        cursor.execute('''
            SELECT * FROM Batting 
            WHERE Innings = ? AND Venue = ? AND Team = ? AND Date = ? AND Player_name = ?
        ''', innings, venue, team, date, player_name)

        existing_player = cursor.fetchone()

        # If the player data already exists, update it
        if existing_player:
            cursor.execute('''
                UPDATE Batting
                SET Dismissal_type = ?, Runs = ?, Balls = ?, Dot_Balls = ?, Strike_Rate = ?, Fours = ?, Sixes = ?
                WHERE Batting_ID = ? AND Innings = ? AND Venue = ? AND Team = ? AND Date = ? AND Player_name = ?
            ''', dismissal_type, r, b, m, sr, fours, sixes, existing_player.Batting_ID, innings, venue, team, date, player_name)

            # Commit the transaction
            conn.commit()

            # Print a success message
            print(f"Values updated for player {player_name}.")
        else:
            # If the player data does not exist, insert it into the database
            cursor.execute('''
                INSERT INTO Batting (Innings, Venue, Team, Date, Player_name, Dismissal_type, Runs, Balls, Dot_Balls, Strike_Rate, Fours, Sixes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', innings, venue, team, date, player_name, dismissal_type, r, b, m, sr, fours, sixes)

            # Commit the transaction
            conn.commit()

            # Print a success message
            print(f"Values inserted for player {player_name}.")

    except Exception as e:
        print(f"Error inserting data for player: {e}")

# Close the connection
conn.close()

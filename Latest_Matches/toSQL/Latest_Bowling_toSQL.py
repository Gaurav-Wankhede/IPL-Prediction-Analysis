import pyodbc
from Latest_Matches.Latest_Bowling import combine_table

# Define your SQL Server connection parameters
server = r'DESKTOP-F8QC9QH\SQLEXPRESS'
database = r'IPL_Prediction_Analysis'

# Define the table name
table_name = 'Bowling'

# Connect to the database
conn = pyodbc.connect(r'DRIVER={SQL Server};'
                      r'SERVER=DESKTOP-F8QC9QH\SQLEXPRESS;'
                      r'DATABASE=IPL_Prediction_Analysis;'
                      r'Trusted_Connection=yes;')

# Check if the table already exists and create it if not
cursor = conn.cursor()
if not cursor.tables(table=table_name, tableType='TABLE').fetchone():
    cursor.execute('''
        CREATE TABLE Bowling (
    Bowling_ID int IDENTITY(1,1) PRIMARY KEY,
    Innings nvarchar(255),
    Venue nvarchar(255),
    Team nvarchar(255),
    Date nvarchar(255),
    Player_name nvarchar(255),
    Overs nvarchar(255),
    Maidens nvarchar(255),
    Runs nvarchar(255),
    Wickets nvarchar(255),
    Economy_rate nvarchar(255),
    Dot_ball nvarchar(255),
    Fours nvarchar(255),
    Sixes nvarchar(255),
    Wides nvarchar(255),
    No_balls nvarchar(255)
)

    ''')
    print(f"Table '{table_name}' created successfully.")

# Commit the transaction
conn.commit()

for player_data in combine_table.itertuples():
    try:
        innings = player_data[1]  # Accessing the first column
        venue = player_data[2]  # Accessing the second column
        team = player_data[3]  # Accessing the third column
        date = player_data[4]  # Accessing the fourth column
        player_name = player_data[5]  # Accessing the fifth column
        overs = player_data[6]  # Accessing the sixth column
        maidens = player_data[7]  # Accessing the seventh column
        runs = player_data[8]  # Accessing the eighth column
        wickets = player_data[9]  # Accessing the ninth column
        economy_rate = player_data[10]  # Accessing the tenth column
        dot_ball = player_data[11]  # Accessing the eleventh column
        fours = player_data[12]  # Accessing the twelfth column
        sixes = player_data[13]  # Accessing the thirteenth column
        wides = player_data[14]  # Accessing the fourteenth column
        no_balls = player_data[15]  # Accessing the fifteenth column

        # Check if the player data already exists in the database
        cursor.execute('''
            SELECT Bowling_ID, * FROM Bowling 
            WHERE Innings = ? AND Venue = ? AND Team = ? AND Date = ? AND Player_name = ?
        ''', innings, venue, team, date, player_name)

        existing_player = cursor.fetchone()

        # If the player data exists, update it in the database
        if existing_player:
            cursor.execute('''
                UPDATE Bowling 
                SET Overs = ?, Maidens = ?, Runs = ?, Wickets = ?, Economy_rate = ?, Dot_ball = ?, Fours = ?, Sixes = ?, Wides = ?, No_balls = ?
                WHERE Bowling_ID = ? AND Innings = ? AND Venue = ? AND Team = ? AND Date = ? AND Player_name = ?
            ''', (overs, maidens, runs, wickets, economy_rate, dot_ball, fours, sixes, wides, no_balls,
                  player_data.Bowling_ID, innings, venue, team, date, player_name))

            # Commit the transaction
            conn.commit()

            # Print a success message
            print(f"Values updated for player {player_name}.")
        else:
            # If the player data does not exist, insert it into the database
            cursor.execute('''
                INSERT INTO Bowling (Bowling_ID, Innings, Venue, Team, Date, Player_name, Overs, Maidens, Runs, Wickets, Economy_rate, Dot_ball, Fours, Sixes, Wides, No_balls)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (player_data.Bowling_ID, innings, venue, team, date, player_name, overs, maidens, runs, wickets,
                  economy_rate, dot_ball, fours, sixes, wides, no_balls))

            # Commit the transaction
            conn.commit()

            # Print a success message
            print(f"Values inserted for player {player_name}.")

    except Exception as e:
        print(f"Error inserting/updating data for player: {e}")

    # Close the connection
conn.close()

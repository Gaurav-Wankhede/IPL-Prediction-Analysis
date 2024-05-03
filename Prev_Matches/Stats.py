import pandas as pd

# Sample raw data
raw_data = """
Team Image
Rajasthan Royals
YK Pathan
T Kohli
9 (3)
17 (15)
7 (12)
SR Watson
YK Pathan
9 (6)
10 (8)
1 (2)
M Kaif
SR Watson
1 (6)
14 (15)
12 (9)
DS Lehmann
M Kaif
1 (2)
6 (8)
4 (6)
M Kaif
RA Jadeja
4 (7)
10 (17)
4 (10)
M Rawat
RA Jadeja
2 (4)
14 (10)
12 (6)
RA Jadeja
D Salunkhe
13 (7)
22 (13)
7 (6)
SK Warne
D Salunkhe
14 (13)
17 (17)
3 (4)
SK Trivedi
D Salunkhe
3 (7)
19* (17)
16 (10)
"""

# Split the raw data by newline character
lines = raw_data.strip().split('\n')

# Create lists to store parsed data
teams = []
partners = []
partnership_runs = []
partnership_balls = []

# Iterate over each line of data
for i in range(1, len(lines), 6):  # Start from 1 to skip the 'Team Image' line
    # Extract team name
    team = lines[i]

    # Extract partner names
    player1_name = lines[i + 1]
    player2_name = lines[i + 2]

    # Extract partnership runs and balls
    partnership_data = lines[i + 3].split()

    # Check if partnership data has the expected format
    if len(partnership_data) >= 2:
        run = partnership_data[0]
        if '(' in partnership_data[1]:
            ball = partnership_data[1].split('(')[1].split('*')[0].replace(')', '')
        else:
            ball = 0  # Set ball to 0 if not provided
        print("Run:", run)
        print("Ball:", ball)

        # Check if run and ball are numeric
        if run.isdigit() and ball.isdigit():
            partnership_runs.append(int(run))
            partnership_balls.append(int(ball))
        else:
            partnership_runs.append(0)
            partnership_balls.append(0)
    else:
        partnership_runs.append(0)
        partnership_balls.append(0)

    # Store data in lists
    teams.append(team)
    partners.append((player1_name, player2_name))

# Create DataFrame
data = {
    'Team': teams,
    'Player1_Name': [p[0] for p in partners],
    'Player2_Name': [p[1] for p in partners],
    'Partnership_Runs': partnership_runs,
    'Partnership_Balls': partnership_balls
}

df = pd.DataFrame(data)

# Rearrange columns
df = df[['Team', 'Player1_Name', 'Player2_Name', 'Partnership_Runs', 'Partnership_Balls']]

print(df)

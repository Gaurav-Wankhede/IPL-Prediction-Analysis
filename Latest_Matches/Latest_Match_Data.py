import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import os
import pyodbc


# Define your SQL Server connection parameters
server = r'DESKTOP-F8QC9QH\SQLEXPRESS'
database = r'IPL_Prediction_Analysis'

# Connect to the database
conn = pyodbc.connect(r'DRIVER={SQL Server};'
                      r'SERVER=' + server + ';'
                      r'DATABASE=' + database + ';'
                      r'Trusted_Connection=yes;')

# Define the cursor
cursor = conn.cursor()

# Define constants
XPATH_DIV_ELEMENT1 = "//div[@class='ds-text-tight-m ds-font-regular ds-text-typo-mid3']"
XPATH_DIV_ELEMENT2 = "//div[@class='ds-flex ds-flex-col ds-mt-3 md:ds-mt-0 ds-mt-0 ds-mb-1']"
XPATH_DIV_ELEMENT3 = "//p[@class='ds-text-tight-s ds-font-medium ds-truncate ds-text-typo']"
XPATH_TEAM1_PLAYED_OVERS = "//*[@id='main-container']/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[2]/div/div[2]/table[1]//span[contains(@class, 'ds-font-regular') and contains(@class, 'ds-text-tight-s') and contains(text(), ' Ov')]"
XPATH_TEAM2_PLAYED_OVERS = '//*[@id="main-container"]/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[3]/div/div[2]/table[1]//span[contains(@class, "ds-font-regular") and contains(@class, "ds-text-tight-s") and contains(text(), " Ov")]'
XPATH_TEAM1_MAX_OVERS = "//*[@id='main-container']/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/span/span[2]"
XPATH_TEAM2_MAX_OVERS = '//*[@id="main-container"]/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[3]/div/div[1]/div/span/span[2]'

# Get the directory of the current script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Construct the absolute path to the file
file_path = os.path.join(dir_path, "match_links.txt")
with open(file_path, 'r') as f:
    match_links = f.read().splitlines()

def process_match_link(driver, link):
    # Load the webpage
    driver.get(link)

    # Wait for elements to be present
    driver.implicitly_wait(1)

    # Find the required div elements using XPath expressions
    div_element1 = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT1)
    div_element2 = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT2)
    div_element3 = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT3)

    # Get the text content of the div elements
    match_info = div_element1.text.split(", ")
    teams_results_text = div_element2.text.split('\n')
    match_result_text = div_element3.text

    # Extracting individual components
    innings, venue = match_info[0], match_info[1]
    date_str = " ".join(match_info[2:4]).replace("Match Date: ", "").replace(",\nIndian Premier League", "").replace(
        ",\nPepsi Indian Premier League", "")

    # Define a function to extract date parts
    def extract_date_parts(date_str):
        # Regular expression pattern to match the date, month, and end day
        match = re.match(r'(\w+)\s+(\d+)(?:\s*-\s*(\d+))?,\s+(\d{4})', date_str)
        if match:
            day = int(match.group(2))
            month = match.group(1)
            end_day = int(match.group(3)) if match.group(3) else day
            year = int(match.group(4))
            return day, month, end_day, year
        else:
            raise ValueError("Invalid date format")

    # Check if the string contains the delimiter " - "
    if " - " in date_str:
        # Extract day, month, year, and end day using the extract_date_parts function
        day, month, end_day, year = extract_date_parts(date_str)
        # Format the date string
        if end_day != day:
            date_str = f"{month} {day}-{end_day} {year}"
            date_str = datetime.strptime(date_str, '%B %d-%d %Y').strftime("%d-%B-%Y")
            print(f"Date: {date_str}")
        else:
            date_str = f"{month} {day} {year}"
            date_str = datetime.strptime(date_str, '%B %d %Y').strftime("%d-%B-%Y")
            print(f"Date: {date_str}")
    date_str = datetime.strptime(date_str, '%B %d %Y').strftime("%d-%B-%Y")

    if len(teams_results_text) >= 4:
        team1, team1_result, team2, team2_result = teams_results_text
    else:
        print(f"Not enough values to unpack in teams_results_text: {teams_results_text}")
        return None

    match_result = match_result_text

    # Initialize variables
    Team1_runs, Team1_wickets, Team2_runs, Team2_wickets, Target, Team1_played_Overs, Team2_played_Overs, Team1_Max_Overs, Team2_Max_Overs = None, None, None, None, None, None, None, None, None

    # Split and extract values for team 1 result
    if team1_result:
        team1_info = team1_result.split('/')
        Team1_runs = re.sub('[^0-9]', '', team1_info[0])
        Team1_wickets = team1_info[1] if len(team1_info) == 2 else "10"
        Team1_played_Overs = driver.find_element(By.XPATH, XPATH_TEAM1_PLAYED_OVERS).text.replace(' Ov', '')

        Team1_Max_Overs = driver.find_element(By.XPATH, XPATH_TEAM1_MAX_OVERS).text
        Team1_Max_Overs = re.sub('[^0-9]', '', Team1_Max_Overs)

        Target = int(Team1_runs) + 1

    # Split and extract values for team 2 result
    if team2_result:
        split_text = team2_result.split(' ')
        Team2_runs = split_text[-1].split('/')[0]
        Team2_wickets = split_text[-1].split('/')[1] if '/' in split_text[-1] else "10"
        Target = int(Team1_runs) + 1 if Team1_runs is not None else None
        Team2_played_Overs = driver.find_element(By.XPATH, XPATH_TEAM2_PLAYED_OVERS).text.replace(" Ov", "")

        Team2_Max_Overs = driver.find_element(By.XPATH, XPATH_TEAM2_MAX_OVERS).text
        Team2_Max_Overs = re.search(r'(\d+)\s+ovs', Team2_Max_Overs).group().replace(" ovs", "")
    print("\nMatch Info:")
    print(f"Inning: {innings}, Venue: {venue}, Date: {date_str}")
    # Print Team1_runs, Team1_wickets, Team2_runs, Team2_wickets,
    print(f"Team1_runs: {Team1_runs}, {Team1_wickets}, Team2_runs: {Team2_runs}, {Team2_wickets}")
    print(f"Team1_played_Overs: {Team1_played_Overs}, {Team1_Max_Overs} Team2_played_Overs: {Team2_played_Overs}, {Team2_Max_Overs}")
    print(f"Target: {Target}, Match_Result: {match_result}")

    # Return the data as a dictionary
    return {
        'Match_ID': None,  # Placeholder for primary key
        'Innings': innings,
        'Venue': venue,
        'Date': date_str,
        'Team1': team1,
        'Team2': team2,
        'Team1_runs': Team1_runs,
        'Team1_wickets': Team1_wickets,
        'Team2_runs': Team2_runs,
        'Team2_wickets': Team2_wickets,
        'Target': Target,
        'Team1_played_Overs': Team1_played_Overs,
        'Team2_played_Overs': Team2_played_Overs,
        'Team1_Max_Overs': Team1_Max_Overs,
        'Team2_Max_Overs': Team2_Max_Overs,
        'Match_Result': match_result
    }

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Initialize an empty list to store the data for all matches
all_matches_data = []

# Fetch the maximum Match_ID from the database
max_match_id_query = "SELECT MAX(Match_ID) AS MaxMatchID FROM Match_Data"
cursor.execute(max_match_id_query)
max_match_id_row = cursor.fetchone()
max_match_id = max_match_id_row[0] if max_match_id_row else 0

# Define a counter for match ID starting from the maximum Match_ID + 1
match_id_counter = max_match_id + 1

# Initialize a set to keep track of unique matches based on the specified columns
unique_matches = set()

# Iterate over all match links
for link in match_links:
    match_data = process_match_link(driver, link)
    if match_data is None:
        print("Match data is not available for this match.")
    elif all(x is None for x in (
            match_data['Team1_runs'], match_data['Team1_wickets'], match_data['Team2_runs'],
            match_data['Team2_wickets'],
            match_data['Target'])):
        print("Match was canceled that day")
    else:
        # Check if the match is unique based on 'Innings', 'Venue', 'Date', 'Team1', and 'Team2'
        match_key = (match_data['Innings'], match_data['Venue'], match_data['Date'], match_data['Team1'], match_data['Team2'])
        if match_key not in unique_matches:
            # Assign the primary key Match_ID
            match_data['Match_ID'] = match_id_counter
            match_id_counter += 1
            # Append the match data to the list of all matches data
            all_matches_data.append(match_data)
            # Add the match key to the set of unique matches
            unique_matches.add(match_key)
        else:
            print("Duplicate match data found. Skipping...")

# Close the driver
driver.close()
# Close the browser
driver.quit()

# Convert the list of all matches data into a DataFrame
df = pd.DataFrame(all_matches_data)

# Print the cleaned DataFrame
print(df)

# Define the table name
table_name = 'Match_Data'

# Insert records into the SQL database
df.to_sql(table_name, conn, if_exists='append', index=False)

# Commit changes and close the database connection
conn.commit()
conn.close()

# Save DataFrame to CSV file
df.to_csv('../Latest_Matches_data.csv', index=False, encoding='utf-8')

import os
import re

import pd
from selenium.webdriver.common.by import By
import pandas as pd
from selenium import webdriver
from io import StringIO
from datetime import datetime

# Define constants
XPATH_DIV_ELEMENT1 = "//div[@class='ds-text-tight-m ds-font-regular ds-text-typo-mid3']"
XPATH_DIV_ELEMENT2 = "//div[@class='ds-flex ds-flex-col ds-mt-3 md:ds-mt-0 ds-mt-0 ds-mb-1']"

# Initialize Selenium WebDriver
driver = webdriver.Chrome()

# Get the directory of the current script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Define the file path for match links
file_path = os.path.join(dir_path, "match_links.txt")

# Read match links from the text file
with open(file_path, 'r') as f:
    All_links = f.read().splitlines()

# Fetch only the batting tables at indices 0 and 2
batting_tables = []
match_info_list = []

for url in All_links:  # Changed from Links to All_links
    while True:
        try:
            driver.get(url)
            html_content = driver.page_source
            break
        except Exception as e:
            print(f"Attempt failed: {e}")

    try:
        # Wrap HTML content in StringIO object
        html_buffer = StringIO(html_content)
        data = pd.read_html(html_buffer)
    except Exception as e:
        print(f"Error parsing HTML content: {e}")
        continue

    # Find the specific div element using the provided XPath expression
    match_info = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT1).text.split(", ")

    # Extracting individual components
    innings = match_info[0]
    venue = match_info[1]
    date_str = " ".join(match_info[2:4]).replace("Match Date: ", "").replace(",\nIndian Premier League", "").replace(
        ",\nPepsi Indian Premier League", "")
    date_str = re.sub(r",\n(?:Indian Premier League|Pepsi Indian Premier League)", "", date_str)

    # Check if the string contains the delimiter " - "
    if " - " in date_str:
        # Split the string by " - " to separate the start and end dates
        date_parts = date_str.split(" - ")

        # Take the first date
        date_to_use = date_parts[0]

        # Update date_str with the first date
        date_str = date_to_use
    else:
        # If the delimiter is not present, use the original string as it is
        date_to_use = date_str

    if date_str:
        # Convert the date string to the desired format
        date_obj = datetime.strptime(date_str, '%B %d %Y')
        # Format the date as 'dd-MMM-YYYY'
        date_str = date_obj.strftime('%d-%b-%Y')

    teams_results_text = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT2).text.split('\n')
    team1 = teams_results_text[0]
    if len(teams_results_text) >= 3:
        team2 = teams_results_text[2]
    else:
        # Handle the case where teams_results_text doesn't have enough elements
        print("Match was Canceled that day.")
        print("\nteams_results_text:", teams_results_text)

    batting_tables.extend([data[0].copy(), data[2].copy()])
    match_info_list.extend([[innings, venue, date_str, team1], [innings, venue, date_str, team2]])

    print("\nMatch Info:")
    print(f"Inning: {innings}, Venue: {venue}, Date: {date_str}")
    print(f"Team 1: {team1}, Team 2: {team2}")
    print(f"Batting Match info list: {match_info_list[-2]} \t {match_info_list[-1]}")


# Define a dictionary of team names and their abbreviations
team_abbreviations = {
    'Chennai Super Kings': 'CSK',
    'Royal Challengers Bengaluru': 'RCB',
    # Add other teams here...
}

combine_table = pd.DataFrame()
for i, table in enumerate(batting_tables):
    match_info = match_info_list[i]
    if 'BATTING' in table.columns:
        # Remove special character Â from the 'BATTING' column
        table['BATTING'] = table['BATTING'].str.replace('Â', '')
        # If large paragraph found from DataFrame then remove it
        table = table[table['BATTING'].str.len() < 300].copy()
        # Process the table further if needed
        table = table.iloc[:-2, :-2]
        table.dropna(inplace=True)

        # Replace the second column name
        table.columns = table.columns[:1].tolist() + ['Dismissal type'] + table.columns[2:].tolist()

        # Remove symbols from the DataFrame
        table = table.apply(
            lambda col: col.astype(str).str.replace(r'[^\w\s]', '', regex=True) if col.name != 'SR' else col)

        # Add new columns for the match info
        table['Innings'], table['Venue'], table['Date'], table['Team'] = match_info

        # Reorder the columns
        table = table[['Innings', 'Venue', 'Team', 'Date'] + [col for col in table.columns if
                                                             col not in ['Innings', 'Venue', 'Team', 'Date']]]

        # Replace full team names with abbreviations
        table['Team'] = table['Team'].map(team_abbreviations).fillna(table['Team'])

        # Add primary key column based on combination of Innings, Venue, Team, and Date
        unique_key = table['Innings'] + '_' + table['Venue'] + '_' + table['Team'] + '_' + table['Date']
        table['Batting_ID'] = range(1, len(table) + 1)
        table.insert(0, 'Batting_ID', table.groupby(unique_key).ngroup() + 1)

        combine_table = pd.concat([combine_table, table], ignore_index=True)

        print(f"Batting Table:")
        print(table)

    else:
        print("Column 'BATTING' not found in the DataFrame.")

# Print the combined table
print("Combine Table:")
print(combine_table)

# Write the combined table to a CSV file
combine_table.to_csv('../Batting_Combine_table.csv', index=False, encoding='utf-8-sig')

# Quit the Selenium WebDriver
driver.quit()

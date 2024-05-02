import os
import pandas as pd
from selenium import webdriver
from io import StringIO
from datetime import datetime
from selenium.webdriver.common.by import By
import re

# Define constants
XPATH_DIV_ELEMENT1 = "/html/body/div[1]/section/section/div[5]/div[1]/div/div[3]/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/div[2]"
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

bowling_tables = []
match_info_list = []
for All_link in All_links:
    while True:
        try:
            driver.get(All_link)
            html_content = driver.page_source
            break
        except Exception as e:
           print(f"Attempt failed: {e}")

    # Find the specific div element using the provided XPath expression
    div_element1 = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT1)
    print("\nBowling Div Element1:\n",div_element1.text)
    div_element2 = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT2)

    # Wrap HTML content in StringIO object
    html_buffer = StringIO(html_content)
    data = pd.read_html(html_buffer)

    match_info = div_element1.text.split(", ")
    print("\n Bowling Match Info:\n", match_info)

    # Extracting individual components
    innings = match_info[0]
    venue = match_info[1]
    date_str = match_info[2:4]  # Take the third and fourth elements after splitting
    date_str[0] = date_str[0].replace("Match Date: ", "")
    date_str[1] = date_str[1].replace(",\nIndian Premier League", "").replace(",\nPepsi Indian Premier League", "")
    date_str = date_str[1].replace(",\nIndian Premier League", "").replace(",\nPepsi Indian Premier League", "")

    date_str = date_str[1].replace(",\nIndian Premier League", "").replace(",\nPepsi Indian Premier League", "")

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

    # Now date_to_use contains the desired date, either the first date from the split operation or the original string

    date_str = " ".join(date_str)

    # Print Extracted components
    print("\nInnings:", innings)
    print("Venue:", venue)
    print("Date:", date_str)

    if date_str:
        # Check if the date string contains the year
        if len(date_str.split()) == 3:  # Assuming the date string format is "Month Day Year"
            date_format = '%B %d %Y'
        else:
            date_format = '%B %d'  # No year in the date string

        # Convert the date string to the desired format
        date_obj = datetime.strptime(date_str, date_format)
        date_str = date_obj.strftime('%d-%b-%Y')

    teams_results_text = div_element2.text.split('\n')
    team1 = teams_results_text[0]

    # Check if teams_results_text has enough elements before accessing index 2
    if len(teams_results_text) >= 3:
        team2 = teams_results_text[2]
        print(f"\nTeam 1: {team1}\nTeam 2: {team2}")
    else:
        # Handle the case where teams_results_text doesn't have enough elements
        print("Match was Canceled that day.")
        print("\nteams_results_text:", teams_results_text)

    # Fetch only the bowling tables at indices 1 and 3
    bowling_tables.append(data[1].copy())
    bowling_tables.append(data[3].copy())
    match_info_list.extend([[innings, venue, date_str, team1], [innings, venue, date_str, team2]])

combine_table = pd.DataFrame()
for i, table in enumerate(bowling_tables):
    table = bowling_tables[i]
    match_info = match_info_list[i]

    # Check if 'BOWLING' column exists in the DataFrame
    if 'BOWLING' in table.columns:
        # Filter out unwanted rows based on specific patterns using regular expressions
        unwanted_pattern = r'^\d+\.\d+\s+to\s+|^\d+\.\d+\s+to\s+|^\d+\.\d+\s+to\s+|leg stump goes for a walk sangakkara exposing all three sticks and trying one of those paddlescoops to fine leg but Gul pitches very full and straight and hits his mark \d+ to DPMD Jayawardene and he wastes no time Begins with a short one which gains on Jayawardene cramped going for the pull shot getting the toe end of the bat on it and it balloons straight to Ganguly at midwicket \d+ to KC sangakkara leg stump goes for a walk sangakkara exposing all three sticks and trying one of those paddlescoops to fine leg but Gul pitches very full and straight and hits his mark \d+'

        table = table[~table['BOWLING'].str.contains(unwanted_pattern)].copy()

        # Remove special character 'Â' from the 'BOWLING' column
        table['BOWLING'] = table['BOWLING'].str.replace('Â', '')
        print("\nRemoving special character\n", table)

        # If large paragraph found from DataFrame then remove it
        table = table[table['BOWLING'].str.len() < 300].copy()

        # Process the table further if needed
        table.dropna(inplace=True)

        # Replace the second column name
        table.columns = table.columns[:1].tolist() + ['Wickets'] + table.columns[2:].tolist()
        print("\nReplacing column name")

        # Remove symbols from the DataFrame
        table = table.apply(
            lambda col: col.astype(str).str.replace(r'[^\w\s]', '', regex=True) if col.name != 'SR' else col)

        # Rename 'BOWLING' column to 'Bowling_Player'
        table.rename(columns={'BOWLING': 'Bowling_Player'}, inplace=True)

        # Add new columns for the match info
        table['Inning'], table['Venue'], table['Date'], table['Team'] = match_info

        # Reorder the columns
        table = table[['Inning', 'Venue', 'Team', 'Date'] + [col for col in table.columns if
                                                             col not in ['Inning', 'Venue', 'Team', 'Date']]]

        # Add primary key column based on uniqueness of 'Inning', 'Venue', 'Team', and 'Date' columns
        unique_key = ['Inning', 'Venue', 'Team', 'Date']
        table_grouped = table.groupby(unique_key)
        table['Bowling_ID'] = table_grouped.ngroup() + 1

        combine_table = pd.concat([combine_table, table], ignore_index=True)
        print(f"\nBowling Table:\n", table)

    else:
        print("Column 'BOWLING' not found in the DataFrame.")

print("\nCombine Table:\n", combine_table)

combine_table.to_csv('../Bowling_Combine_table.csv', index=False, encoding='utf-8-sig')

# Quit the Selenium WebDriver
driver.quit()

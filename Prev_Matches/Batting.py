import os
import re
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from io import StringIO
from dateutil.parser import parse
def batting():
    # Define constants
    XPATH_DIV_ELEMENT1 = "//div[@class='ds-text-tight-m ds-font-regular ds-text-typo-mid3']"
    XPATH_DIV_ELEMENT2 = "//div[@class='ds-flex ds-flex-col ds-mt-3 md:ds-mt-0 ds-mt-0 ds-mb-1']"

    # Define the function to extract date parts
    # Define the function to extract date parts using re.split
    def extract_date_parts(date_str):
        # Split the date string by spaces, hyphens, or commas
        parts = [part for part in re.split(r'\s+|-|,', date_str) if part]
        if len(parts) < 3:
            raise ValueError("Invalid date format")

        month = parts[0]
        day = int(parts[1])
        end_day = int(parts[2]) if len(parts) == 4 else day  # Adjust the index to correctly get the end day
        year = int(parts[-1])
        return day, month, end_day, year

    # Initialize Selenium WebDriver
    driver = webdriver.Chrome()

    # Create a directory named 'links'
    if not os.path.exists('links'):
        os.makedirs('links')
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

    for url in All_links:
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
        date_str = ", ".join(match_info[2:4])  # Include the year in the date string

        # Remove non-date information from date_str
        date_str = date_str.split('\n')[0]

        # Check if the string contains the delimiter " - "
        if " - " in date_str:
            # Extract day, month, year, and end day using the extract_date_parts function
            day, month, end_day, year = extract_date_parts(date_str)
            # Format the date string
            start_date_str = parse(f"{month} {day}, {year}").strftime("%d-%B-%Y")
            end_date_str = parse(f"{month} {end_day}, {year}").strftime("%d-%B-%Y")
            print(f"\nStart Date: {start_date_str}")
            print(f"End Date: {end_date_str}")
        else:
            date_str = date_str.strip()  # Remove leading and trailing spaces
            start_date_str = parse(date_str).strftime("%d-%B-%Y")
            end_date_str = start_date_str
            print(f"\nStart Date: {start_date_str}")
            print(f"End Date: {end_date_str}")

        teams_results_text = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT2).text.split('\n')
        team1 = teams_results_text[0]
        team2 = teams_results_text[2] if len(teams_results_text) >= 3 else ""

        batting_tables.extend([data[0].copy(), data[2].copy()])
        match_info_list.extend([[innings, venue, start_date_str, end_date_str, team1],
                                [innings, venue, start_date_str, end_date_str, team2]])

        print("Match Info:")
        print(f"Inning: {innings}, Venue: {venue}, Start Date: {start_date_str}, End Date: {end_date_str}")
        print(f"Team 1: {team1}, Team 2: {team2}")
        print(f"Batting Match info list: {match_info_list[-2]} \t {match_info_list[-1]}")

    # Define a dictionary of team names and their abbreviations
    team_abbreviations = {
        'Chennai Super Kings': 'CSK',
        'Royal Challengers Bengaluru': 'RCB',
        # Add other teams here...
    }

    combine_table = pd.DataFrame()  # Initialize combine_table outside the loop

    for i, table in enumerate(batting_tables):
        match_info = match_info_list[i]
        if 'BATTING' in table.columns:
            table['BATTING'] = table['BATTING'].str.replace('Â', '')
            table = table[table['BATTING'].str.len() < 300].copy()
            table = table.iloc[:-2, :-2]
            table.dropna(inplace=True)
            table.columns = table.columns[:1].tolist() + ['Dismissal type'] + table.columns[2:].tolist()
            table = table.apply(
                lambda col: col.astype(str).str.replace(r'[^\w\s]', '', regex=True) if col.name != 'SR' else col)
            table['Innings'], table['Venue'], table['Start Date'], table['End Date'], table['Team'] = match_info
            table = table[['Innings', 'Venue', 'Team', 'Start Date', 'End Date'] + [col for col in table.columns if
                                                                                    col not in ['Innings', 'Venue',
                                                                                                'Team', ' Start Date',
                                                                                                'End Date']]]
            table['Team'] = table['Team'].map(team_abbreviations).fillna(table['Team'])

            table.reset_index(drop=True, inplace=True)

            print("Table:")
            print(table)

            # Check for duplicate columns and remove them
            table = table.loc[:, ~table.columns.duplicated()]

            combine_table = pd.concat([combine_table, table], ignore_index=True)  # Concatenate DataFrames

            # Reset index after concatenation
            combine_table.reset_index(drop=True, inplace=True)

            # Create a new column 'Batting_ID' with a range from 1 to the length of the DataFrame plus 1
            combine_table['Batting_ID'] = range(1, len(combine_table) + 1)

            # Move the 'Batting_ID' column to the first position
            cols = combine_table.columns.tolist()
            cols.insert(0, cols.pop(cols.index('Batting_ID')))


            # Check for duplicate column labels
            if len(set(cols)) != len(cols):
                raise ValueError("Duplicate column labels detected")

            # Reindex the DataFrame only if there are no duplicate column labels
            combine_table = combine_table.reindex(columns=cols)

            print(f"Combined Table:")
            print(combine_table)

        else:
            print("Column 'BATTING' not found in the DataFrame.")

    # Print the combined table
    print("Combine Table:")
    print(combine_table)

    # Write the combined table to a CSV file
    combine_table.to_csv('../../csv/Batting_table.csv', index=False, encoding='utf-8-sig')

    # Quit the Selenium WebDriver
    driver.quit()

    return combine_table
import os
import re
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from io import StringIO
from dateutil.parser import parse

def batting():
    # Define constants
    XPATH_DIV_ELEMENT1 = "//div[@class='ds-text-tight-m ds-font-regular ds-text-typo-mid3']"
    XPATH_DIV_ELEMENT2 = "//div[@class='ds-flex ds-flex-col ds-mt-3 md:ds-mt-0 ds-mt-0 ds-mb-1']"

    # Define the function to extract date parts
    def extract_date_parts(date_str):
        parts = [part for part in re.split(r'\s+|-|,', date_str) if part]
        if len(parts) < 3:
            raise ValueError("Invalid date format")

        month = parts[0]
        day = int(parts[1])
        end_day = int(parts[2]) if len(parts) == 4 else day
        year = int(parts[-1])
        return day, month, end_day, year

    driver = webdriver.Chrome()

    # Create a directory named 'links'
    if not os.path.exists('links'):
        os.makedirs('links')

    dir_path = os.path.dirname(os.path.realpath(__file__))

    file_path = os.path.join(dir_path, "Match_Links.txt")

    with open(file_path, 'r') as f:
        All_links = f.read().splitlines()

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
            html_buffer = StringIO(html_content)
            data = pd.read_html(html_buffer)
        except Exception as e:
            print(f"Error parsing HTML content: {e}")
            continue

        match_info = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT1).text.split(", ")

        innings = match_info[0]
        venue = match_info[1]
        date_str = ", ".join(match_info[2:4])

        date_str = date_str.split('\n')[0]

        if " - " in date_str:
            day, month, end_day, year = extract_date_parts(date_str)
            start_date_str = parse(f"{month} {day}, {year}").strftime("%d-%B-%Y")
            end_date_str = parse(f"{month} {end_day}, {year}").strftime("%d-%B-%Y")
            print(f"\nStart Date: {start_date_str}")
            print(f"End Date: {end_date_str}")
        else:
            date_str = date_str.strip()
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

    team_abbreviations = {
        'Chennai Super Kings': 'CSK',
        'Royal Challengers Bengaluru': 'RCB',
        # Add other teams here...
    }

    combine_table = pd.DataFrame()

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

            table = table.loc[:, ~table.columns.duplicated()]

            combine_table = pd.concat([combine_table, table], ignore_index=True)

            combine_table.reset_index(drop=True, inplace=True)

            combine_table['Batting_ID'] = range(1, len(combine_table) + 1)

            cols = combine_table.columns.tolist()
            cols.insert(0, cols.pop(cols.index('Batting_ID')))

            if len(set(cols)) != len(cols):
                raise ValueError("Duplicate column labels detected")

            combine_table = combine_table.reindex(columns=cols)

            print(f"Combined Table:")
            print(combine_table)

        else:
            print("Column 'BATTING' not found in the DataFrame.")

    print("Combine Table:")
    print(combine_table)

    # Ensure the directory exists
    if not os.path.exists('./csv'):
        os.makedirs('./csv')

    # Save the DataFrame to a CSV file
    combine_table.to_csv('./csv/Batting_table.csv', index=False, encoding='utf-8-sig')

    driver.quit()

    return combine_table
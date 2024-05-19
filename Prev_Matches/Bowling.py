from selenium import webdriver
from selenium.webdriver.common.by import By
from io import StringIO
import os
import pandas as pd
import re
from dateutil.parser import parse


def extract_date_parts(date_str):
    parts = [part for part in re.split(r'\s+|-|,', date_str) if part]
    if len(parts) < 3:
        raise ValueError("Invalid date format")

    month = parts[0]
    day = int(parts[1])
    end_day = int(parts[2]) if len(parts) == 4 else day
    year = int(parts[-1])
    return day, month, end_day, year


def bowling():
    driver = webdriver.Chrome()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "match_links.txt")

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

        XPATH_DIV_ELEMENT1 = "/html/body/div[1]/section/section/div[5]/div[1]/div/div[3]/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/div[2]"
        XPATH_DIV_ELEMENT2 = "//div[@class='ds-flex ds-flex-col ds-mt-3 md:ds-mt-0 ds-mt-0 ds-mb-1']"

        div_element1 = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT1)
        div_element2 = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT2)

        html_buffer = StringIO(html_content)
        data = pd.read_html(html_buffer)

        match_info = div_element1.text.split(", ")

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

        teams_results_text = div_element2.text.split('\n')
        team1 = teams_results_text[0]

        if len(teams_results_text) >= 3:
            team2 = teams_results_text[2]
        else:
            print("Match was Canceled that day.")
            print("\nteams_results_text:", teams_results_text)

        bowling_tables.append(data[1].copy())
        bowling_tables.append(data[3].copy())
        match_info_list.extend([[innings, venue, start_date_str, end_date_str, team1],
                                [innings, venue, start_date_str, end_date_str, team2]])

        print("\nMatch Info:")
        print(f"Inning: {innings}, Venue: {venue}, Date: {start_date_str}, {end_date_str}")
        print(f"Team 1: {team1}, Team 2: {team2}")
        print(f"Bowling Match info list: {match_info_list[-2]} \t {match_info_list[-1]}")

    combine_table = pd.DataFrame()
    unique_columns = set()

    for i, table in enumerate(bowling_tables):
        table = bowling_tables[i]
        match_info = match_info_list[i]

        if 'BOWLING' in table.columns:
            unwanted_pattern = r'^\d+\.\d+\s+to\s+|^\d+\.\d+\s+to\s+|^\d+\.\d+\s+to\s+|leg stump goes for a walk sangakkara exposing all three sticks and trying one of those paddlescoops to fine leg but Gul pitches very full and straight and hits his mark \d+ to DPMD Jayawardene and he wastes no time Begins with a short one which gains on Jayawardene cramped going for the pull shot getting the toe end of the bat on it and it balloons straight to Ganguly at midwicket \d+ to KC sangakkara leg stump goes for a walk sangakkara exposing all three sticks and trying one of those paddlescoops to fine leg but Gul pitches very full and straight and hits his mark \d+'

            table = table[~table['BOWLING'].str.contains(unwanted_pattern)].copy()

            table['BOWLING'] = table['BOWLING'].str.replace('Â', '')

            table = table[table['BOWLING'].str.len() < 300].copy()

            table.dropna(inplace=True)

            table.columns = table.columns[:1].tolist() + ['Wickets'] + table.columns[2:].tolist()

            table = table.apply(
                lambda col: col.astype(str).str.replace(r'[^\w\s]', '', regex=True) if col.name != 'SR' else col)

            table.rename(columns={'BOWLING': 'Bowling_Player'}, inplace=True)

            table['Inning'], table['Venue'], table['Start Date'], table['End Date'], table['Team'] = match_info

            table = table[['Inning', 'Venue', 'Team', 'Start Date', 'End Date'] + [col for col in table.columns if
                                                                                   col not in ['Inning', 'Venue',
                                                                                               'Team', 'Start Date',
                                                                                               'End Date']]]

            combine_table = pd.concat([combine_table, table], ignore_index=True)
            print(f"\nBowling Table:\n", table)

        else:
            print("Column 'BOWLING' not found in the DataFrame.")

    combine_table = combine_table.loc[:, ~combine_table.columns.duplicated()]

    print("\nCombine Table:\n", combine_table)

    combine_table.to_csv('../Bowling_Combine_table.csv', index=False, encoding='utf-8-sig')

    driver.quit()

    return combine_table

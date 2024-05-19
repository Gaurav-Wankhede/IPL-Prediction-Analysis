def latest_bowling():
    import os
    import pandas as pd
    from selenium import webdriver
    from io import StringIO
    from selenium.webdriver.common.by import By
    import re
    from dateutil.parser import parse

    # Define constants
    XPATH_DIV_ELEMENT1 = "/html/body/div[1]/section/section/div[5]/div[1]/div/div[3]/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/div[2]"
    XPATH_DIV_ELEMENT2 = "//div[@class='ds-flex ds-flex-col ds-mt-3 md:ds-mt-0 ds-mt-0 ds-mb-1']"

    # Define the function to extract date parts
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
        div_element2 = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT2)

        # Wrap HTML content in StringIO object
        html_buffer = StringIO(html_content)
        data = pd.read_html(html_buffer)

        match_info = div_element1.text.split(", ")

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

        teams_results_text = div_element2.text.split('\n')
        team1 = teams_results_text[0]

        # Check if teams_results_text has enough elements before accessing index 2
        if len(teams_results_text) >= 3:
            team2 = teams_results_text[2]
        else:
            # Handle the case where teams_results_text doesn't have enough elements
            print("Match was Canceled that day.")
            print("\nteams_results_text:", teams_results_text)

        # Fetch only the bowling tables at indices 1 and 3
        bowling_tables.append(data[1].copy())
        bowling_tables.append(data[3].copy())
        match_info_list.extend([[innings, venue, start_date_str, end_date_str, team1],
                                    [innings, venue, start_date_str, end_date_str, team2]])

        print("\nMatch Info:")
        print(f"Inning: {innings}, Venue: {venue}, Date: {start_date_str}, {end_date_str}")
        print(f"Team 1: {team1}, Team 2: {team2}")
        print(f"Bowling Match info list: {match_info_list[-2]} \t {match_info_list[-1]}")


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
            table['Inning'], table['Venue'], table['Start Date'], table['End Date'], table['Team'] = match_info

            # Reorder the columns
            table = table[['Inning', 'Venue', 'Team', 'Start Date', 'End Date'] + [col for col in table.columns if
                                                                 col not in ['Inning', 'Venue', 'Team', 'Start Date', 'End Date']]]

            # Add primary key column based on uniqueness of 'Inning', 'Venue', 'Team', and 'Date' columns
            unique_key = ['Inning', 'Venue', 'Team', 'Start Date', 'End Date']
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

    return combine_table
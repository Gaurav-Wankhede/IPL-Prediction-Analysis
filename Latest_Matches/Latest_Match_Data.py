def latest_match_data():
    import re
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from datetime import datetime
    import os
    from dateutil.parser import parse

    # Define constants
    XPATH_DIV_ELEMENT1 = "//div[@class='ds-text-tight-m ds-font-regular ds-text-typo-mid3']"
    XPATH_DIV_ELEMENT2 = "//div[@class='ds-flex ds-flex-col ds-mt-3 md:ds-mt-0 ds-mt-0 ds-mb-1']"
    XPATH_DIV_ELEMENT3 = "//p[@class='ds-text-tight-s ds-font-medium ds-truncate ds-text-typo']"
    XPATH_TEAM1_PLAYED_OVERS = "//*[@id='main-container']/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[2]/div/div[2]/table[1]//span[contains(@class, 'ds-font-regular') and contains(@class, 'ds-text-tight-s') and contains(text(), ' Ov')]"
    XPATH_TEAM2_PLAYED_OVERS = '//*[@id="main-container"]/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[3]/div/div[2]/table[1]//span[contains(@class, "ds-font-regular") and contains(@class, "ds-text-tight-s") and contains(text(), " Ov")]'
    XPATH_TEAM1_MAX_OVERS = "//*[@id='main-container']/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/span/span[2]"
    XPATH_TEAM2_MAX_OVERS = '//*[@id="main-container"]/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[3]/div/div[1]/div/span/span[2]'

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

    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Construct the absolute path to the file
    file_path = os.path.join(dir_path, "match_links.txt")
    with open(file_path, 'r') as f:
        match_links = f.read().splitlines()

    # Define the function to process each match link
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
        print(f"Inning: {innings}, Venue: {venue}, Date: {start_date_str}, {end_date_str}")
        # Print Team1_runs, Team1_wickets, Team2_runs, Team2_wickets,
        print(f"Team1_runs: {Team1_runs}, {Team1_wickets}, Team2_runs: {Team2_runs}, {Team2_wickets}")
        print(f"Team1_played_Overs: {Team1_played_Overs}, {Team1_Max_Overs} Team2_played_Overs: {Team2_played_Overs}, {Team2_Max_Overs}")
        print(f"Target: {Target}, Match_Result: {match_result}")

        # Return the data as a dictionary
        return {
            'Match_ID': None,  # Placeholder for primary key
            'Innings': innings,
            'Venue': venue,
            'Start_Date': start_date_str,
            'End_Date': end_date_str,
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

    # Define a counter for match ID
    match_id_counter = 1

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
            match_key = (match_data['Innings'], match_data['Venue'], match_data['Start_Date'], match_data['End_Date'], match_data['Team1'], match_data['Team2'])
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

    # Save DataFrame to CSV file
    df.to_csv('../Matches_data.csv', index=False, encoding='utf-8')

    # Return the DataFrame
    return df
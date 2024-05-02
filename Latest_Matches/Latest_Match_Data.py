from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import Latest_Match_Link
import re

# Define constants
XPATH_DIV_ELEMENT1 = "//div[@class='ds-text-tight-m ds-font-regular ds-text-typo-mid3']"
XPATH_DIV_ELEMENT2 = "//div[@class='ds-flex ds-flex-col ds-mt-3 md:ds-mt-0 ds-mt-0 ds-mb-1']"
XPATH_DIV_ELEMENT3 = "//p[@class='ds-text-tight-s ds-font-medium ds-truncate ds-text-typo']"
XPATH_TEAM1_PLAYED_OVERS = "//*[@id='main-container']/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[2]/div/div[2]/table[1]/tbody/tr[23]/td[2]/span[1]"

def process_match_link(driver, link):
    # Load the webpage
    while True:
        try:
            driver.get(link)
            break  # Exit the loop if the get operation is successful
        except Exception as e:
            # Handle the exception (if any) and continue the loop
            print(f"Error occurred: {e}")

    # Find the required div elements using XPath expressions
    div_element1 = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT1)  # For innings, venue, and date
    print(div_element1.text)
    div_element2 = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT2)  # For teams and results
    print(div_element2.text)
    div_element3 = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT3)  # For match result
    print(div_element3.text)

    # Get the text content of the div elements
    match_info = div_element1.text.split(", ")
    print(match_info)
    teams_results_text = div_element2.text.split('\n')
    print(teams_results_text)
    match_result_text = div_element3.text
    print(match_result_text)

    # Extracting individual components
    innings = match_info[0]
    print(innings)
    venue = match_info[1]
    print(venue)
    date_str = match_info[2:4]# Take the third and fourth elements after splitting
    date_str[0] = date_str[0].replace("Match Date: ", "")
    date_str[1] = date_str[1].replace(",\nIndian Premier League", "")
    print(date_str)
    date_str = " ".join(date_str)
    print(date_str)
    if date_str:
        # Convert the date string to the desired format
        date_obj = datetime.strptime(date_str, '%B %d %Y')
        print(date_obj)
        # Format the date as 'dd-MMM-YYYY'
        date_str = date_obj.strftime('%d-%b-%Y')
        print(date_str)
    else:
        date_str = ""

    team1 = teams_results_text[0]
    print(team1)
    team1_result = teams_results_text[1]
    print(team1_result)
    team2 = teams_results_text[2]
    print(team2)
    team2_result = teams_results_text[3]
    print(team1_result)
    match_result = match_result_text

    # Initialize variables
    Team1_runs = Team1_wickets = Team2_runs = Team2_wickets = Target = Team1_played_Overs = Team2_played_Overs = None

    # Split and extract values for team 1 result
    if team1_result:
        team1_info = team1_result.split('/')
        if len(team1_info) == 2:
            Team1_runs, Team1_wickets = map(int, team1_info)
        else:
            Team1_runs = int(team1_info[0])
            Team1_wickets = "10"

    # If Team1_wickets does not exist, find the element with the given XPath and print its text value in Team1_played_Overs
    if Team1_wickets is None:
        Team1_played_Overs = driver.find_element(By.XPATH, XPATH_TEAM1_PLAYED_OVERS).text
        print(Team1_played_Overs)
    else:
        # Set Team1_played_Overs to always be 20
        Team1_played_Overs = "20"

    # Split and extract values for team 2 result
    if team2_result:
        split_text = team2_result.split(' ')

        # Extract Team2_runs and Team2_wickets
        if split_text:
            team2_info = split_text[-1].split('/')
            if len(team2_info) >= 2:
                Team2_runs = int(team2_info[0])
                print("Team2_runs", Team2_runs)
                Team2_wickets = int(team2_info[1])
                print("Team2_wickets", Team2_wickets)
            else:
                Team2_runs = int(team2_info[0])
                print("Team2_runs", Team2_runs)
                Team2_wickets = "10"
                print("Team2_wickets", Team2_wickets)
            # Extract Target as Team1_runs + 1
            if Team1_runs is not None:
                Target = Team1_runs + 1

            # Extract Team2_played_Overs
            Team2_played_Overs = split_text[0].split('(')[1]
            Team2_played_Overs = re.sub(' [oO]v,', '', Team2_played_Overs)

    # Create a DataFrame
    data = {
        'Innings': [innings],
        'Venue': [venue],
        'Date': [date_str],
        'Team1': [team1],
        'Team2': [team2],
        'Team1_runs': [Team1_runs],
        'Team1_wickets': [Team1_wickets],
        'Team2_runs': [Team2_runs],
        'Team2_wickets': [Team2_wickets],
        'Target': [Target],
        'Team1_played_Overs': [Team1_played_Overs],
        'Team2_played_Overs': [Team2_played_Overs],
        'Match_Result': [match_result]}

    return data

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Fetch all match links
match_links = Latest_Match_Link.fetch_match_links()
print(match_links)

# Initialize an empty list to store the data for all matches
all_matches_data = []

# Iterate over all match links
for link in match_links:
    try:
        match_data = process_match_link(driver, link)
        # Append the data for this match to the list
        all_matches_data.append(match_data)
    except Exception as e:
        print(f"An error occurred while processing the match link {link}: {e}")

# Close the browser
driver.quit()

# Convert the list of all matches data into a DataFrame
df = pd.DataFrame(all_matches_data)

# Apply the 'replace' function to the DataFrame
df = df.astype(str).replace(["\\[", "\\]", "\\(", "\\)", "'"], "", regex=True)

#split Team2_played_Overs column by / and I have to use 1st element
if 'Team2_played_Overs' in df.columns:
    df['Team2_played_Overs'] = df['Team2_played_Overs'].apply(lambda x: x.split('/')[0] if '/' in x else '20')
else:
    print("Column 'Team2_played_Overs' does not exist in the DataFrame.")

# Print the DataFrame
print(df)

# Save DataFrame to CSV file
df.to_csv('../Latest_2024_Matches_data.csv', index=False, encoding='utf-8')

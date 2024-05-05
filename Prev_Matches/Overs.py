import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from datetime import datetime
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Define your SQL Server connection parameters
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, "Overs_Comparison_Links.txt")

# Read links from the file
with open(file_path, "r") as file:
    links = file.readlines()

# Initialize the WebDriver
driver = webdriver.Chrome()

# Initialize lists to store data
all_data = []

# Initialize Over_ID counter
over_id_counter = 1

# Define a function to extract the day, month, and end day separately from the date string
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

# Iterate over each link
for link in links:
    try:
        # Fetch the link
        link = link.strip()

        # Open the link
        driver.get(link)

        # Wait for the container to be clickable
        container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                f"/html/body/div[1]/section/section/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[1]/div")))
        print(f"Expanding container 1: {container.text}")
        container.click()

        # Find team names
        team1_name = driver.find_element(By.XPATH,
                                         "//*[@id='main-container']/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[2]/table//th[2]").text
        print(f"Team1: {team1_name}")
        team2_name = driver.find_element(By.XPATH,
                                         "//*[@id='main-container']/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[2]/table//th[3]").text
        print(f"Team2: {team2_name}")

        # Find match info
        match_info = driver.find_element(By.XPATH,
                                         "//div[@class='ds-text-tight-m ds-font-regular ds-text-typo-mid3']").text.split(
            ", ")
        innings = match_info[0]
        venue = match_info[1]
        date_str = " ".join(match_info[2:4]).replace("Match Date: ", "").replace(",\nIndian Premier League",
                                                                                 "").replace(
            ",\nPepsi Indian Premier League", "")
        date_str = re.sub(r",\n(?:Indian Premier League|Pepsi Indian Premier League)", "", date_str)

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

        # Find all rows in the table
        rows = driver.find_elements(By.XPATH,
                                    "//*[@id='main-container']/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[2]/table//tr")

        # Initialize lists to store data for this particular link
        team1_overs = []
        team1_runs = []
        team1_wickets = []
        team1_total_runs = []
        team1_total_wickets = []

        team2_overs = []
        team2_runs = []
        team2_wickets = []
        team2_total_runs = []
        team2_total_wickets = []

        # Iterate over rows and extract data
        for row_index, row in enumerate(rows[1:], start=1):  # Skip the header row
            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) >= 3:  # Check if cells list has at least 3 elements
                overs_value = cells[0].text
                team1_data = cells[1].text.split("/")
                team2_data = cells[2].text.split("/")

                if len(team1_data) > 1:
                    team1_overs.append(overs_value)
                    team1_runs.append(re.sub(r'\D', '', team1_data[1].split("(")[1].split(")")[0].split(",")[0]))
                    team1_wickets.append(re.sub(r'\D', '', team1_data[1].split("(")[1].split(")")[0].split(",")[1]))
                    team1_total_runs.append(team1_data[0])
                    team1_total_wickets.append(team1_data[1].split("(")[0])

                if len(team2_data) > 1:
                    team2_overs.append(overs_value)
                    team2_runs.append(re.sub(r'\D', '', team2_data[1].split("(")[1].split(")")[0].split(",")[0]))
                    team2_wickets.append(re.sub(r'\D', '', team2_data[1].split("(")[1].split(")")[0].split(",")[1]))
                    team2_total_runs.append(team2_data[0])
                    team2_total_wickets.append(team2_data[1].split("(")[0])

        # Create DataFrames for each team for this particular link
        team1_df = pd.DataFrame({
            "Over_ID": range(over_id_counter, over_id_counter + len(team1_overs)),
            "Innings": [innings] * len(team1_overs),
            "Venue": [venue] * len(team1_overs),
            "Date": [date_str] * len(team1_overs),
            "Team_Name": [team1_name] * len(team1_overs),
            "Overs": team1_overs,
            "Team_Runs": team1_runs,
            "Team_Wickets": team1_wickets,
            "Team_Total_Runs": team1_total_runs,
            "Team_Total_Wickets": team1_total_wickets
        })

        team2_df = pd.DataFrame({
            "Over_ID": range(over_id_counter + len(team1_overs), over_id_counter + len(team1_overs) + len(team2_overs)),
            "Innings": [innings] * len(team2_overs),
            "Venue": [venue] * len(team2_overs),
            "Date": [date_str] * len(team2_overs),
            "Team_Name": [team2_name] * len(team2_overs),
            "Overs": team2_overs,
            "Team_Runs": team2_runs,
            "Team_Wickets": team2_wickets,
            "Team_Total_Runs": team2_total_runs,
            "Team_Total_Wickets": team2_total_wickets
        })

        # Concatenate DataFrames for this particular link
        link_data = pd.concat([team1_df, team2_df], ignore_index=True)
        print("\n", link_data)
        # Append data for this particular link to the list of all data
        all_data.append(link_data)

        # Update the Over_ID counter for the next table
        over_id_counter += len(team1_overs) + len(team2_overs)

    except (TimeoutException, NoSuchElementException) as e:
        print(f"An error occurred while processing the link: {link}")
        print(e)
        continue

# Close the WebDriver
driver.quit()

# Concatenate DataFrames for all links
df = pd.concat(all_data, ignore_index=True)

print(df)

# Export DataFrame to CSV
df.to_csv("../Overs.csv", index=False)

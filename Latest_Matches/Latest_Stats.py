import os
import pandas as pd
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pyodbc


# Define your SQL Server connection parameters
server = r'DESKTOP-F8QC9QH\SQLEXPRESS'
database = r'IPL_Prediction_Analysis'

# Connect to the database
conn = pyodbc.connect(r'DRIVER={SQL Server};'
                      r'SERVER=' + server + ';'
                      r'DATABASE=' + database + ';'
                      r'Trusted_Connection=yes;')

# Create a cursor
cursor = conn.cursor()

# Fetch the maximum Stats_ID from the Stats_Data table
cursor.execute("SELECT MAX(Stats_ID) FROM Stats_Data")
max_stats_id = cursor.fetchone()[0]
mvp_id_counter = max_stats_id + 1 if max_stats_id else 1

# XPath for the div element
XPATH_DIV_ELEMENT1 = "//div[@class='ds-text-tight-m ds-font-regular ds-text-typo-mid3']"

# Construct the absolute path to the file
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, "Stats_Links.txt")

# Read links from the file
with open(file_path, "r") as file:
    links = file.readlines()

# Initialize the WebDriver
driver = webdriver.Chrome()

data = []

for i, link in enumerate(links):
    print(f"Processing link: {link}")
    # Navigate to the link
    driver.get(link.strip())
    print("Navigated to link")

    # Wait for the specific element to become available
    wait = WebDriverWait(driver, 10)  # wait for up to 10 seconds
    specific_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-container"]/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[3]/div[2]')))
    print("Found specific element")

    # Find the specific div element using the provided XPath expression
    match_info = driver.find_element(By.XPATH, XPATH_DIV_ELEMENT1).text.split(", ")

    # Extracting individual components
    innings = match_info[0]
    venue = match_info[1]
    date_str = " ".join(match_info[2:4]).replace("Match Date: ", "").replace(",\nIndian Premier League", "").replace(
        ",\nPepsi Indian Premier League", "")
    date_str = re.sub(r",\n(?:Indian Premier League|Pepsi Indian Premier League)", "", date_str)

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

    # Convert the date string to the desired format
    if date_str:
        date_obj = datetime.strptime(date_str, '%B %d %Y')
        date_str = date_obj.strftime('%d-%b-%Y')

    # XPaths for the team containers
    xpaths = ['//*[@id="main-container"]/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[4]/div[2]/div/div[2]/div[1]/div/div[1]',
              '//*[@id="main-container"]/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[4]/div[2]/div/div[2]/div[2]/div/div[1]']

    # XPaths for the first page
    first_page_xpaths = ['//*[@id="main-container"]/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[3]/div[2]/div/div[2]/div[1]',
                         '//*[@id="main-container"]/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[3]/div[2]/div/div[2]/div[2]']

    # Use the first page XPaths for the first link, and the regular XPaths for the rest
    current_xpaths = first_page_xpaths if i == 0 else xpaths

    for j, xpath in enumerate(current_xpaths):
        try:
            # Find the team container using the XPath
            container = specific_element.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            # If the first XPath doesn't work, try the other one
            container = specific_element.find_element(By.XPATH, first_page_xpaths[j] if i != 0 else xpaths[j])
        print(f"Found team container {j + 1}")

        # Find the team using the CSS selector within the container
        team = container.find_element(By.TAG_NAME, 'span').text

        # Find the elements using the CSS selector within the container
        elements = container.find_elements(By.CSS_SELECTOR, '.ds-flex.ds-justify-between')

        partnership_scores_list = []
        for element in elements:
            # From the element, find the partnership score using the CSS selector
            partnership_scores = element.find_elements(By.CSS_SELECTOR, '.ds-text-tight-s.ds-font-medium')

            for partnership_score in partnership_scores:
                # Add the partnership score to the list
                partnership_scores_list.append(partnership_score.text)

        # Assign the scores to the correct variables
        for k in range(0, len(partnership_scores_list), 5):
            Player1 = partnership_scores_list[k]
            Player2 = partnership_scores_list[k + 1]
            Player1_Runs, Player1_Balls = re.findall(r'\d+', partnership_scores_list[k + 2]) if re.findall(r'\d+', partnership_scores_list[k + 2]) else ("", "")
            Partnership_Runs, Partnership_Balls = re.findall(r'\d+', partnership_scores_list[k + 3]) if re.findall(r'\d+', partnership_scores_list[k + 3]) else ("", "")
            Player2_Runs, Player2_Balls = re.findall(r'\d+', partnership_scores_list[k + 4]) if re.findall(r'\d+', partnership_scores_list[k + 4]) else ("", "")

            # Append the data to the list when all variables are set
            data.append([mvp_id_counter, innings, venue, date_str, team, Player1, Player2, Player1_Runs, Player1_Balls, Partnership_Runs, Partnership_Balls, Player2_Runs, Player2_Balls])
            print(data)

            # Update the counter
            mvp_id_counter += 1

# Close the driver
driver.quit()

# Create DataFrame
df = pd.DataFrame(data, columns=['Stats_ID', 'Innings', 'Venue', 'Date', 'Team', 'Player 1', 'Player 2', 'Player 1 Runs', 'Player 1 Balls', 'Partnership Runs', 'Partnership Balls', 'Player 2 Runs', 'Player 2 Balls'])
print(df)

# Export DataFrame to CSV
df.to_csv('../Latest_Stats.csv', index=False)

# Close the cursor and connection
cursor.close()
conn.close()

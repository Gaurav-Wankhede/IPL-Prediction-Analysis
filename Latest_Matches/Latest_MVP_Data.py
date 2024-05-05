import os
import pandas as pd
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from io import StringIO
import pyodbc


# Function to fetch table data from a URL using XPath
def fetch_table_data(driver, url, xpath):
    try:
        driver.get(url)
        table = driver.find_element(By.XPATH, xpath)

        # You can then extract data from the table as needed
        table_html = table.get_attribute('outerHTML')
        df = pd.read_html(StringIO(table_html))[0]  # Wrap HTML string in StringIO object
        return df
    except Exception as e:
        print("Error:", e)
        return None

# Configure Selenium WebDriver
driver = webdriver.Chrome()

# Construct the absolute path to the file
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, "MVP_Links.txt")

# Read links from MVP_Links.txt file
with open(file_path, "r") as file:
    links = file.readlines()

# Create an empty list to store the table data
data_list = []

# XPath for the div element
XPATH_DIV_ELEMENT1 = "//div[@class='ds-text-tight-m ds-font-regular ds-text-typo-mid3']"

# Initialize a counter for MVP_ID
mvp_id_counter = 1

# Connect to the database
server = r'DESKTOP-F8QC9QH\SQLEXPRESS'
database = r'IPL_Prediction_Analysis'
conn = pyodbc.connect(r'DRIVER={SQL Server};'
                      r'SERVER=' + server + ';'
                      r'DATABASE=' + database + ';'
                      r'Trusted_Connection=yes;')
cursor = conn.cursor()

# Get the maximum MVP_ID from the MVP_Data table
cursor.execute("SELECT MAX(MVP_ID) FROM MVP_Data")
max_mvp_id = cursor.fetchone()[0]

# If max_mvp_id is None, set it to 0
max_mvp_id = max_mvp_id if max_mvp_id is not None else 0

# Iterate through each link and fetch table data
for link in links:
    link = link.strip()  # Remove leading/trailing whitespaces
    table_data = fetch_table_data(driver, link,
                                  '//*[@id="main-container"]/div[5]/div[1]/div/div[3]/div[1]/div[2]/div/div[2]/div/table')
    if table_data is not None:
        # Extract header and data rows separately
        header = table_data.iloc[0]
        table_data = table_data[0:]

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
                date_str = f"{day}-{month} - {end_day}-{month}, {year}"
                print(f"Date: {date_str}")
            else:
                date_str = f"{day}-{month}, {year}"
                print(f"Date: {date_str}")

        # Rename columns to match the required column names
        table_data.columns = ["Player_Name", "Team", "Total_Impact", "Runs", "Impact_Runs", "Batting_Impact", "Bowl",
                              "Impact_Wickets", "Bowling_Impact"]

        # Add new columns for the match info
        table_data['Innings'], table_data['Venue'], table_data['Date'] = innings, venue, date_str

        # Add 'MVP_ID' column with unique ID for each row
        table_data['MVP_ID'] = range(max_mvp_id + mvp_id_counter, max_mvp_id + mvp_id_counter + len(table_data))

        # Reorder the columns
        cols = ['MVP_ID', 'Innings', 'Venue', 'Date', 'Player_Name', 'Team'] + [col for col in table_data.columns if
                                                                                col not in ['MVP_ID', 'Innings',
                                                                                            'Venue', 'Date',
                                                                                            'Player_Name', 'Team']]
        table_data = table_data[cols]

        print(table_data)
        # Append table data to the list
        data_list.append(table_data)
# Concatenate all tables in the list to form the final DataFrame
final_data = pd.concat(data_list, ignore_index=True)

# Split 'Runs' into 'Runs' and 'Balls_Faced'
final_data[['Runs', 'Balls_Faced']] = final_data['Runs'].str.split('(', expand=True)

# Remove the closing parenthesis from 'Balls_Faced'
final_data['Balls_Faced'] = final_data['Balls_Faced'].str.replace(')', '')
# Convert 'Runs' and 'Balls_Faced' to integers
final_data['Runs'] = final_data['Runs'].astype(int)
final_data['Balls_Faced'] = final_data['Balls_Faced'].astype(int)

# Split 'Bowl' into 'Wickets' and 'Runs_Conceded'
final_data[['Wickets', 'Runs_Conceded']] = final_data['Bowl'].str.split('/', expand=True)
# Remove any extra characters if present
final_data['Wickets'] = final_data['Wickets'].str.replace('[^0-9]', '')
final_data['Runs_Conceded'] = final_data['Runs_Conceded'].str.replace('[^0-9]', '')

# Convert 'Wickets' and 'Runs_Conceded' to integers
final_data['Wickets'] = final_data['Wickets'].astype(int)
final_data['Runs_Conceded'] = final_data['Runs_Conceded'].astype(int)
print(final_data)
# Save the final DataFrame to a CSV file
final_data.to_csv("Latest_MVP_Data.csv", index=False)

# Quit the WebDriver after processing all links
driver.quit()
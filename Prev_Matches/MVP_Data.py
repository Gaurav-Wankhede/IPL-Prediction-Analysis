import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from io import StringIO


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


# Function to generate sequential MVP_ID
def generate_mvp_ids(df, start_id):
    df.insert(0, 'MVP_ID', range(start_id, start_id + len(df)))
    return df


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

# Initialize start ID
start_id = 1

# Modify required columns to match the actual column names extracted from the table data
required_columns = ["PLAYER", "Team", "TI", "Runs", "R. Impact", "Bowl", "Bo. Wkts", "Bo. Impact"]

# Iterate through each link and fetch table data
for link in links:
    link = link.strip()  # Remove leading/trailing whitespaces
    table_data = fetch_table_data(driver, link,
                                  '//*[@id="main-container"]/div[5]/div[1]/div/div[3]/div[1]/div[2]/div/div[2]/div/table')
    if table_data is not None:
        # Extract header and data rows separately
        header = table_data.iloc[0]
        table_data = table_data[1:]

        # Rename columns to match the required column names
        table_data.columns = ["Player_Name", "Team", "Total_Impact", "Runs", "Impact_Runs", "Batting_Impact", "Bowl",
                              "Impact_Wickets", "Bowling_Impact"]

        # Generate sequential MVP_ID for the current table
        table_data = generate_mvp_ids(table_data, start_id)

        # Update start ID for the next table
        start_id += len(table_data)

        # Append table data to the list
        data_list.append(table_data)
        print(table_data)
# Concatenate all tables in the list to form the final DataFrame
final_data = pd.concat(data_list, ignore_index=True)

# Save the final DataFrame to a CSV file
final_data.to_csv("MVP_Data.csv", index=False)

# Quit the WebDriver after processing all links
driver.quit()

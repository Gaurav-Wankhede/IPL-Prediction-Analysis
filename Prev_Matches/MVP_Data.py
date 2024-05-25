def mvp_data():
    import os
    import pandas as pd
    import re
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from io import StringIO
    from dateutil.parser import parse

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

    # Initialize Selenium WebDriver with headless option

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
            date_str = " ".join(match_info[2:4]).replace("Match Date: ", "").replace(",\nIndian Premier League",
                                                                                     "").replace(
                ",\nPepsi Indian Premier League", "")
            date_str = re.sub(r",\n(?:Indian Premier League|Pepsi Indian Premier League)", "", date_str)

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

            # Rename columns to match the required column names
            table_data.columns = ["Player_Name", "Team", "Total_Impact", "Runs", "Impact_Runs", "Batting_Impact",
                                  "Bowl",
                                  "Impact_Wickets", "Bowling_Impact"]

            # Add new columns for the match info
            table_data['Innings'], table_data['Venue'], table_data['Start_Date'], table_data[
                'End_Date'] = innings, venue, start_date_str, end_date_str

            # Add 'MVP_ID' column with unique ID for each row
            table_data['MVP_ID'] = range(mvp_id_counter, mvp_id_counter + len(table_data))

            # Update the counter
            mvp_id_counter += len(table_data)

            # Reorder the columns
            cols = ['MVP_ID', 'Innings', 'Venue', 'Start_Date', 'End_Date', 'Player_Name', 'Team'] + [col for col in
                                                                                                      table_data.columns
                                                                                                      if
                                                                                                      col not in [
                                                                                                          'MVP_ID',
                                                                                                          'Innings',
                                                                                                          'Venue',
                                                                                                          'Start_Date',
                                                                                                          'End_Date',
                                                                                                          'Player_Name',
                                                                                                          'Team']]
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
    final_data['Runs'] = final_data['Runs'].apply(lambda x: 0 if x == '-' else int(x))
    final_data['Balls_Faced'] = final_data['Balls_Faced'].apply(lambda x: 0 if x is None or x == '-' else int(x))

    # Split 'Bowl' into 'Wickets' and 'Runs_Conceded'
    final_data[['Wickets', 'Runs_Conceded']] = final_data['Bowl'].str.split('/', expand=True)
    # Remove any extra characters if present
    final_data['Wickets'] = final_data['Wickets'].str.replace('[^0-9]', '')
    final_data['Runs_Conceded'] = final_data['Runs_Conceded'].str.replace('[^0-9]', '')

    # Ensure the directory exists
    if not os.path.exists('./csv'):
        os.makedirs('./csv')

    # Save the final DataFrame to a CSV file
    final_data.to_csv("./csv/MVP_Data.csv", index=False)

    # Quit the WebDriver after processing all links
    driver.quit()

    return final_data



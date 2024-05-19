def latest_stats():
    import os
    import pandas as pd
    import re
    from selenium import webdriver
    from selenium.common import NoSuchElementException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from dateutil.parser import parse

    # XPath for the div element
    XPATH_DIV_ELEMENT1 = "//div[@class='ds-text-tight-m ds-font-regular ds-text-typo-mid3']"

    # Initialize a counter for MVP_ID
    mvp_id_counter = 1

    # Construct the absolute path to the file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "Stats_Links.txt")

    # Read links from the file
    with open(file_path, "r") as file:
        links = file.readlines()

    # Initialize the WebDriver
    driver = webdriver.Chrome()

    data = []

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

        # XPaths for the team containers
        xpaths = ['//*[@id="main-container"]/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[4]/div[2]/div/div[2]/div[1]',
                  '//*[@id="main-container"]/div[5]/div[1]/div/div[3]/div[1]/div[2]/div[4]/div[2]/div/div[2]/div[2]']

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
            team = container.find_element(By.CSS_SELECTOR, '.ds-text-tight-m.ds-font-bold').text

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
                data.append([mvp_id_counter, innings, venue, start_date_str, end_date_str, team, Player1, Player2, Player1_Runs, Player1_Balls, Partnership_Runs, Partnership_Balls, Player2_Runs, Player2_Balls])
                print(data)

                # Update the counter
                mvp_id_counter += 1

    # Close the driver
    driver.quit()

    df = pd.DataFrame(data, columns=['Stats_ID', 'Innings', 'Venue', 'Start Date', 'End Date', 'Team', 'Player 1', 'Player 2', 'Player 1 Runs', 'Player 1 Balls', 'Partnership Runs', 'Partnership Balls', 'Player 2 Runs', 'Player 2 Balls'])
    print(df)
    df.to_csv('../Stats.csv', index=False)

    return df
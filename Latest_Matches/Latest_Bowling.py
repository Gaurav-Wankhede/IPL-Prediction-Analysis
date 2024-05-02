from selenium.webdriver.common.by import By
import Latest_Match_Link
import pandas as pd
from selenium import webdriver
from io import StringIO
from datetime import datetime

# Define constants
XPATH_DIV_ELEMENT1 = "//div[@class='ds-text-tight-m ds-font-regular ds-text-typo-mid3']"
XPATH_DIV_ELEMENT2 = "//div[@class='ds-flex ds-flex-col ds-mt-3 md:ds-mt-0 ds-mt-0 ds-mb-1']"

# Initialize Selenium WebDriver
driver = webdriver.Chrome()

Links = Latest_Match_Link.fetch_match_links()

# Define a dictionary of team names and their abbreviations
team_abbreviations = {
    'Chennai Super Kings': 'CSK',
    'Royal Challengers Bengaluru': 'RCB',
    # Add other teams here...
}

bowling_tables = []
match_info_list = []
for url in Links:
    try:
        driver.get(url)
        html_content = driver.page_source

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
        date_str = match_info[2:4]  # Take the third and fourth elements after splitting
        date_str[0] = date_str[0].replace("Match Date: ", "")
        date_str[1] = date_str[1].replace(",\nIndian Premier League", "")
        date_str = " ".join(date_str)
        if date_str:
            # Convert the date string to the desired format
            date_obj = datetime.strptime(date_str, '%B %d %Y')
            # Format the date as 'dd-MMM-YYYY'
            date_str = date_obj.strftime('%d-%b-%Y')

        teams_results_text = div_element2.text.split('\n')
        team1 = teams_results_text[0]
        team2 = teams_results_text[2]

        bowling_tables.extend([data[1].copy(), data[3].copy()])
        match_info_list.extend([[innings, venue, date_str, team1], [innings, venue, date_str, team2]])
    except Exception as e:
        print("Error fetching URL:", url)
        print(e)

combine_table = pd.DataFrame()
for i in range(len(bowling_tables)):
    table = bowling_tables[i]
    match_info = match_info_list[i]

    if 'BOWLING' in table.columns:
        # Filter out unwanted rows based on specific patterns using regular expressions
        unwanted_pattern = r'^\d+\.\d+\s+to\s+|^\d+\.\d+\s+to\s+|^\d+\.\d+\s+to\s+|leg stump goes for a walk sangakkara exposing all three sticks and trying one of those paddlescoops to fine leg but Gul pitches very full and straight and hits his mark \d+ to DPMD Jayawardene and he wastes no time Begins with a short one which gains on Jayawardene cramped going for the pull shot getting the toe end of the bat on it and it balloons straight to Ganguly at midwicket \d+ to KC sangakkara leg stump goes for a walk sangakkara exposing all three sticks and trying one of those paddlescoops to fine leg but Gul pitches very full and straight and hits his mark \d+'

        table = table[~table['BOWLING'].str.contains(unwanted_pattern)].copy()
        print("Removing unwanted rows")
        print(table)
        # Remove special character 'Â' from the 'BOWLING' column
        table['BOWLING'] = table['BOWLING'].str.replace('Â', '')
        print("Removing special character")
        print(table)

        # If large paragraph found from DataFrame then remove it
        table = table[table['BOWLING'].str.len() < 300].copy()
        print("Removing large paragraph")
        print(table)

        # Process the table further if needed
        table.dropna(inplace=True)
        print("Removing NaN")
        print(table)

        # Replace the second column name
        table.columns = table.columns[:1].tolist() + ['Wickets'] + table.columns[2:].tolist()
        print("Replacing column name")

        # Remove symbols from the DataFrame
        table = table.apply(
            lambda col: col.astype(str).str.replace(r'[^\w\s]', '', regex=True) if col.name != 'SR' else col)
        print("Removing symbols")
        print(table)

        # Add new columns for the match info
        table['Inning'], table['Venue'], table['Date'], table['Team'] = match_info

        # Reorder the columns
        table = table[['Inning', 'Venue', 'Team', 'Date'] + [col for col in table.columns if
                                                             col not in ['Inning', 'Venue', 'Team', 'Date']]]

        # Replace full team names with abbreviations
        table['Team'] = table['Team'].map(team_abbreviations).fillna(table['Team'])

        combine_table = pd.concat([combine_table, table], ignore_index=True)
        print(f"Bowling Table:")
        print(table)

    else:
        print("Column 'BOWLING' not found in the DataFrame.")

print("Combine Table:")
print(combine_table)

combine_table.to_csv('../Latest_Bowling_Combine_table.csv', index=False)

# Quit the Selenium WebDriver
driver.quit()

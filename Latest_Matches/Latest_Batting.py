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

# Fetch only the batting tables at indices 0 and 2
batting_tables = []
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

        batting_tables.extend([data[0].copy(), data[2].copy()])
        match_info_list.extend([[innings, venue, date_str, team1], [innings, venue, date_str, team2]])
    except Exception as e:
        print("Error fetching URL:", url)
        print(e)

# Define a dictionary of team names and their abbreviations
team_abbreviations = {
    'Chennai Super Kings': 'CSK',
    'Royal Challengers Bengaluru': 'RCB',
    # Add other teams here...
}

combine_table = pd.DataFrame()
for i in range(len(batting_tables)):
    table = batting_tables[i]
    match_info = match_info_list[i]

    if 'BATTING' in table.columns:
        # Remove special character Â from the 'BATTING' column
        table['BATTING'] = table['BATTING'].str.replace('Â', '')
        # If large paragraph found from DataFrame then remove it
        table = table[table['BATTING'].str.len() < 300].copy()
        # Process the table further if needed
        table = table.iloc[:-2, :-2]
        table.dropna(inplace=True)
        # Replace the second column name
        table.columns = ['Batting_Player'] + ['Dismissal type'] + table.columns[2:].tolist()
        # Remove symbols from the DataFrame
        table = table.apply(
            lambda col: col.astype(str).str.replace(r'[^\w\s]', '', regex=True) if col.name != 'SR' else col)
        # Remove 5th column
        table = table.drop(table.columns[4], axis=1)

        # Add new columns for the match info
        table['Inning'], table['Venue'], table['Date'], table['Team'] = match_info

        # Reorder the columns
        table = table[['Inning', 'Venue', 'Team', 'Date'] + [col for col in table.columns if
                                                             col not in ['Inning', 'Venue', 'Team', 'Date']]]

        # Replace full team names with abbreviations
        table['Team'] = table['Team'].map(team_abbreviations).fillna(table['Team'])

        combine_table = pd.concat([table, combine_table], ignore_index=True)

    combine_table.to_csv('../Latest_Batting_Combine_table.csv', index=False, encoding='utf-8-sig')
print("Combine Table:")
print(combine_table)
# Quit the Selenium WebDriver
driver.quit()
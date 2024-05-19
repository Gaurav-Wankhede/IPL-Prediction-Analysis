from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import Season

def fetch_links():
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    # Fetch all season URLs
    season_urls = Season.season_urls

    print(f"Season URLs: {season_urls}")

    all_links = {}

    try:
        for season_url in season_urls:
            # Extract the year from the season_url
            year = season_url.split('/')[-1]

            print(f"Year: {year}")

            print(f"\n\nFetching links from: {season_url}\n")
            # Load the webpage
            driver.get(season_url)

            # Find the specific div element using the provided class name
            div_element = driver.find_element(By.CLASS_NAME, 'ds-p-0')

            if div_element:
                # Find all links within the div element
                for link in div_element.find_elements(By.TAG_NAME, 'a'):
                    href = link.get_attribute('href')
                    if href and href.endswith('full-scorecard'):
                        print(f"\nFull Scorecard: {href}")
                        if year not in all_links:
                            all_links[year] = []
                        all_links[year].append(href)
                        # Replace 'full-scorecard' with other patterns
                        for pattern in ['match-impact-player', 'match-statistics', 'match-overs-comparison', 'points-table-standings']:
                            replaced_link = href.replace('full-scorecard', pattern)
                            print(f"{pattern.capitalize()}: {replaced_link}")
                            all_links[year].append(replaced_link)

    finally:
        # Close the browser
        driver.quit()

    return all_links

def write_links_to_file(links, output_file):
    # Create a directory named 'links'
    if not os.path.exists('links'):
        os.makedirs('links')

    for year, year_links in links.items():
        # Modify the file path to include the 'links' directory
        with open(os.path.join('links', f"{output_file}_{year}.txt"), "w") as file:
            for link in year_links:
                file.write(link + "\n")

# Fetch all links and replace 'full-scorecard' with other patterns
all_links = fetch_links()

# Write each type of link to its corresponding file
write_links_to_file({year: [link for link in year_links if 'full-scorecard' in link] for year, year_links in all_links.items()}, 'Match_data')
write_links_to_file({year: [link for link in year_links if 'match-impact-player' in link] for year, year_links in all_links.items()}, 'MVP_data')
write_links_to_file({year: [link for link in year_links if 'match-statistics' in link] for year, year_links in all_links.items()}, 'Stats_data')
write_links_to_file({year: [link for link in year_links if 'match-overs-comparison' in link] for year, year_links in all_links.items()}, 'Overs_Comparison_data')
write_links_to_file({year: [link for link in year_links if 'points-table-standings' in link] for year, year_links in all_links.items()}, 'Points_Table_data')

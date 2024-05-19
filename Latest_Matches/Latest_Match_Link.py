def latest_match_link():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from Latest_Matches import Latest_Season

    def fetch_links():
        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome()

        # Fetch the season URL
        season_url = Latest_Season.season_url
        print("Navigating to:", season_url)

        # Load the webpage
        driver.get(season_url)

        # Find the specific div element using the provided XPath expression
        div_element = driver.find_element(By.XPATH, "//div[@class='ds-p-0']")

        all_links = []

        if div_element:
            # Find all links within the div element
            for link in div_element.find_elements(By.TAG_NAME, 'a'):
                href = link.get_attribute('href')
                if href and href.endswith('full-scorecard'):
                    print(f"\nFull Scorecard: {href}")
                    all_links.append(href)
                    # Replace 'full-scorecard' with other patterns
                    for pattern in ['match-impact-player', 'match-statistics', 'match-overs-comparison', 'points-table-standings']:
                        replaced_link = href.replace('full-scorecard', pattern)
                        print(f"{pattern.capitalize()}: {replaced_link}")
                        all_links.append(replaced_link)

        # Close the browser
        driver.quit()

        return all_links

    def write_links_to_file(links, output_file):
        with open(f"{output_file}", "w") as file:
            for link in links:
                file.write(link + "\n")

    # Fetch all links
    all_links = fetch_links()

    # Write each type of link to its corresponding file
    write_links_to_file([link for link in all_links if 'full-scorecard' in link], 'Match_Links.txt')
    write_links_to_file([link for link in all_links if 'match-impact-player' in link], 'MVP_Links.txt')
    write_links_to_file([link for link in all_links if 'match-statistics' in link], 'Stats_Links.txt')
    write_links_to_file([link for link in all_links if 'match-overs-comparison' in link], 'Overs_Comparison_Links.txt')
    write_links_to_file([link for link in all_links if 'points-table-standings' in link], 'Points_Table_Links.txt')

    return all_links
from selenium import webdriver
from selenium.webdriver.common.by import By
import Season


def fetch_match_links():
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    # Fetch all season URLs
    season_urls = Season.season_urls

    All_Match_Links = []

    try:
        with open("Match_Links.txt", "w") as file:
            for season_url in season_urls:
                # Load the webpage
                driver.get(season_url)

                # Find the specific div element using the provided XPath expression
                div_element = driver.find_element(By.XPATH, "//div[@class='ds-p-0']")

                match_links = []
                if div_element:
                    # Find all links within the div element
                    for link in div_element.find_elements(By.TAG_NAME, 'a'):
                        href = link.get_attribute('href')
                        if href and href.endswith('full-scorecard'):  # Check if href ends with 'full-scorecard'
                            match_links.append(href)
                            file.write(href + "\n")  # Write the link to the file
                            print(f"Match link: {href}")

                    All_Match_Links.extend(match_links)

        return All_Match_Links
    finally:
        # Close the browser
        driver.quit()


# Example usage:
match_links = fetch_match_links()


def fetch_mvp_links(season_urls):
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    All_MVP_Links = []

    try:
        with open("MVP_Links.txt", "w") as file:
            for season_url in season_urls:
                # Load the webpage
                driver.get(season_url)

                # Find the specific div element using the provided XPath expression
                div_element = driver.find_element(By.XPATH, "//div[@class='ds-p-0']")

                mvp_links = []
                if div_element:
                    # Find all links within the div element
                    for link in div_element.find_elements(By.TAG_NAME, 'a'):
                        href = link.get_attribute('href')
                        if href and href.endswith('full-scorecard'):
                            # Replace 'full-scorecard' with 'match-impact-player'
                            href = href.replace('full-scorecard', 'match-impact-player')
                            mvp_links.append(href)
                            file.write(href + "\n")  # Write the link to the file

                    All_MVP_Links.extend(mvp_links)

        return All_MVP_Links
    finally:
        # Close the browser
        driver.quit()


# Example usage:
season_urls = Season.season_urls

# Fetch MVP links for all seasons
mvp_links = fetch_mvp_links(season_urls)

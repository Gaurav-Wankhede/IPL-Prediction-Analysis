from selenium import webdriver
from selenium.webdriver.common.by import By
import Latest_Season

def fetch_match_links():
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    # Fetch the season URL
    season_url = Latest_Season.season_url
    print("Navigating to:", season_url)

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
                print(f"Match link: {href}")

    # Close the browser
    driver.quit()

    return match_links


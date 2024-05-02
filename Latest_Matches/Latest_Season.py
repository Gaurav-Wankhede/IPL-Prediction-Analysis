from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



# Define the patterns
pattern = "indian-premier-league-2024-1410320"

# Create a list of URLs for each season
season_url = f"https://www.espncricinfo.com/series/{pattern}/match-schedule-fixtures-and-results"

# Set up the Chrome driver
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.quit()
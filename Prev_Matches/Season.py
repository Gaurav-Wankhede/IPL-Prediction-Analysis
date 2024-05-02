import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# Define the patterns
patterns = (
    "indian-premier-league-2007-08-313494",
    "indian-premier-league-2009-374163",
    "indian-premier-league-2009-10-418064",
    "indian-premier-league-2011-466304",
    "indian-premier-league-2012-520932",
    "indian-premier-league-2013-586733",
    "pepsi-indian-premier-league-2014-695871",
    "pepsi-indian-premier-league-2015-791129",
    "ipl-2016-968923",
    "ipl-2017-1078425",
    "ipl-2018-1131611",
    "ipl-2019-1165643",
    "ipl-2020-21-1210595",
    "ipl-2021-1249214",
    "indian-premier-league-2022-1298423",
    "indian-premier-league-2023-1345038")

# Create a list of URLs for each season
season_urls = [f"https://www.espncricinfo.com/series/{pattern}/match-schedule-fixtures-and-results" for pattern in patterns]

# Set up the Chrome driver
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

driver.quit()
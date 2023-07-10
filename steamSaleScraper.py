from bs4 import BeautifulSoup as bs
import pandas
import requests
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

# TARGET: The number of games we want to scrape from steam
TARGET = 300

# URL
url = "https://store.steampowered.com/search/?specials=1&os=win"

# Webdriver options
options = webdriver.ChromeOptions()
options.headless = True

# Set up webdriver object
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(url)

# Parse games from the get request results (HTTP)
games = driver.find_elements(By.CLASS_NAME, "search_result_row")

# If we haven't gotten enough games, scroll to the bottom of the page, wait, and update gamesFound
currHeight = driver.execute_script('return document.body.scrollHeight')
while len(games)  < TARGET:
    # Scroll
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 

    # Wait for new content to load at the bottom
    time.sleep(3)

    # Check page height
    newHeight = driver.execute_script('return document.body.scrollHeight')

    # Exit if no new content loaded in
    if newHeight == currHeight:
        break
    
    # Update current page height
    currHeight = newHeight

    # Update games and loop
    games = driver.find_elements(By.CLASS_NAME, "search_result_row")

# Report what we found
print("Found " + str(len(games)) + " games.")



# Set up what will be transfered to our CSV file
headers = ["Game Title", "Discount", "Original Price", "Discounted Price"]
records = [] 

for element in games:
    # Create a new dictionary (hashmap) for our games 
    newRecord = {}
    newRecord["Game Title"] = element.find_element(By.CLASS_NAME, "title").text
    newRecord["Discount"] = element.find_element(By.CLASS_NAME, "search_discount").text

    prices = element.find_element(By.CLASS_NAME, "search_price").text.split("\n")
    # This item wasn't discounted
    if len(prices) < 2:
        continue

    # Store Prices
    newRecord["Original Price"] = prices[0].strip()
    newRecord["Discounted Price"] = prices[1].strip()

    # Add new Record to Table for CSV
    records.append(newRecord)

# Now we're on to writing our output. Let's get the date
currDate = date.today()
currDateFormatted = str(currDate.month) + "-" + str(currDate.day) + "-" + str(currDate.year)  

# create a CSV
with open("SteamSales_" + currDateFormatted + ".csv", "w+", encoding="utf-8") as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames=headers, lineterminator='\n')
    writer.writeheader()
    writer.writerows(records)

# create a text file with a beautified table output from our csv using panda
with open("SteamSales_" + currDateFormatted + ".txt", "w+", encoding="utf-8") as txtFile:
    dataFrame = pandas.read_csv("SteamSales_" + currDateFormatted + ".csv", encoding="utf-8")
    dataFrame = dataFrame.sort_values(by="Discount", ascending=False)
    txtFile.write(dataFrame.to_markdown(index=False));
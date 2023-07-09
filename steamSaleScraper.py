from bs4 import BeautifulSoup as bs
import pandas
import requests
import sys
from datetime import date
import csv

# URL
url = "https://store.steampowered.com/search/?specials=1&os=win"

# HTTP req
data = requests.get(url)

# Parse HTML
html = bs(data.text, "html.parser")
games = html.select("div.responsive_search_name_combined")

# Assemble our headers for our CSV output
headers = ["Game Title", "Discount", "Original Price", "Discounted Price"]
records = [] # Records for our CSV output

for game in games:
    newRecord = {}
    newRecord["Game Title"] = game.select("span.title")[0].get_text()
    newRecord["Discount"] = game.select("div.col.search_discount.responsive_secondrow")[0].get_text().strip()

    # Sometimes games that aren't on sale appear. Ignore these
    if len(game.select("div.col.search_price.discounted.responsive_secondrow")) < 1:
        continue
    else:
        prices = game.select("div.col.search_price.discounted.responsive_secondrow")[0].get_text().strip().split("$")
        newRecord["Original Price"] = ("$" + prices[1])
        newRecord["Discounted Price"] = ("$" + prices[2])
    
    # Add new Record to Table for CSV
    records.append(newRecord)


# Now we're on to writing our output. Let's get the date
currDate = date.today()
currDateFormatted = str(currDate.month) + "-" + str(currDate.day) + "-" + str(currDate.year)  

# create a CSV
with open("SteamSales_" + currDateFormatted + ".csv", "w+", encoding="utf-8") as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(records)

# create a text file with a beautified table output from our csv using panda
with open("SteamSales_" + currDateFormatted + ".txt", "w+", encoding="utf-8") as txtFile:
    dataFrame = pandas.read_csv("SteamSales_" + currDateFormatted + ".csv", encoding="utf-8")
    dataFrame = dataFrame.sort_values(by="Discount", ascending=False)
    txtFile.write(dataFrame.to_markdown(index=False));
    #txtFile.write(pandas.read_csv("SteamSales_" + currDateFormatted + ".csv", encoding="utf-8").to_markdown(index=False))

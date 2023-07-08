from bs4 import BeautifulSoup as bs
import requests
import sys
from datetime import date

# Open a txtfile to write to
currDate = date.today()
currDateFormatted = str(currDate.month) + "-" + str(currDate.day) + "-" + str(currDate.year)  
sys.stdout = open("SteamSales_" + currDateFormatted  + ".txt", "w")

# URL
url = "https://store.steampowered.com/search/?specials=1&os=win"

# HTTP req
data = requests.get(url)

# Parse HTML
html = bs(data.text, "html.parser")
games = html.select("div.responsive_search_name_combined")

for game in games:
    title = game.select("span.title")[0].get_text()
    discount = game.select("div.col.search_discount.responsive_secondrow")[0].get_text().strip()

    # Sometimes games that aren't on sale appear. Ignore these
    if len(game.select("div.col.search_price.discounted.responsive_secondrow")) < 1:
        continue
    else:
        prices = game.select("div.col.search_price.discounted.responsive_secondrow")[0].get_text().strip().split("$")
        price = "$" + prices[1]
        newPrice = "$" + prices[2]

    print("{: >60}: {: >8} -> ({: >5}) -> {: >8} \
          ".format(title, price, discount, newPrice))

# Now that we've printed to this new file, close it up
sys.stdout.close()
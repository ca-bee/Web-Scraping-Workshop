import requests
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd

URL = "https://quotes.toscrape.com"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')

# prettify gives us the content of the html of the site in an easy-to-read format 
# print(soup.prettify)

quotes = []
# Note: find only finds the first div specified; use findAll to get all of them.
table = soup.findAll("div", attrs={"class": "quote"})
# num = 1
for line in table:
    quote = {}
    quote["Author"] = line.find("small", attrs={"class": "author"}).string
    quote["Lines"] = line.find("span", attrs={"class": "text"}).string
    # print(num, ": ", quote["lines"], " by ", quote["author"])
    quotes.append(quote)
    # num += 1

# gets the end of the url for the next page
getNextQuotes = soup.findAll("li", attrs={"class": "next"})
if not getNextQuotes:
    tailURL = ""
else:
    for next in getNextQuotes:
        tailURL = next.find("a")["href"]
        # print(tailURL)

def repeatRequest(tURL):
    # we concatenate it with our original URL
    fullURL = URL + tURL
    # print(fullURL)
    r2 = requests.get(fullURL)
    soup2 = BeautifulSoup(r2.content, "html5lib")

    table2 = soup2.findAll("div", attrs={"class": "quote"})
    fullQuotes = []

    # num = 1
    for x in table2:
        quote = {}
        quote["Lines"] = x.find("span", attrs={"class": "text"}).string
        quote["Author"] = x.find("small", attrs={"class": "author"}).string
        # print(num, ": ", quote["lines"], " by ", quote["author"])
        fullQuotes.append(quote)
        # num += 1

    getNextQuotes = soup2.findAll("li", attrs={"class": "next"})
    if not getNextQuotes:
        return fullQuotes, ""
    
    for next in getNextQuotes:
        tURL = next.find("a")["href"]
    
    return fullQuotes, tURL

while tailURL:
    fullQuotes, tailURL = repeatRequest(tailURL)
    print(tailURL)
    quotes.extend(fullQuotes)
    # print(quotes)


# Writing to csv files
fields = ["Lines", "Author"]
filename = "quote_list.csv"
f = open(filename, "w", encoding="utf-8")

# Use "w" to clear and write to file the first time, then use append afterwards to add to it.
with f as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(quotes)

f.close()

df = pd.read_csv("quote_list.csv")
df.to_html("index.html")
# To delete the csv file afterwards
#os.remove("quote_list.csv")
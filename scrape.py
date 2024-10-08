import requests
from bs4 import BeautifulSoup
# import os
import csv

# Enter the URL of the site you are scraping
URL="https://quotes.toscrape.com"
r=requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')
# To get a better formatted visual representation:
print(soup.prettify)

quotes=[]
# Note: find only finds the first div specified; use findAll to get all of them.
table = soup.findAll("div", attrs={"class": "quote"})
num = 1
for x in table:
    quote = {}
    quote["author"] = x.find("small", attrs={"class": "author"}).string
    quote["lines"] = x.find("span", attrs={"class": "text"}).string
    #quote["author"] = x.find("small", attrs={"class": "author"}).string
    print(num, ": ", quote["lines"], " by ", quote["author"])
    quotes.append(quote)
    num +=1

# gets the end of the url for the next page
getNextQuotes = soup.findAll("li", attrs={"class": "next"})
count = str(2)
for link in getNextQuotes:
    # We're getting the URL of the next page
    tailURL = link.find("a")["href"]

# we concatenate it with our original URL
tailURL = URL + tailURL

r2 = requests.get(tailURL)
soup2 = BeautifulSoup(r2.content, "html5lib")
print(soup2.prettify)

# Note: find only finds the first div specified; use findAll to get all of them.
table = soup2.findAll("div", attrs={"class": "quote"})
num = 1
for x in table:
    quote = {}
    quote["author"] = x.find("small", attrs={"class": "author"}).string
    quote["lines"] = x.find("span", attrs={"class": "text"}).string
    #quote["author"] = x.find("small", attrs={"class": "author"}).string
    print(num, ": ", quote["lines"], " by ", quote["author"])
    quotes.append(quote)
    num +=1

# Writing to csv files
fields = ["lines", "author"]
filename = "quote_list.csv"

# Use "w" to clear and write to file the first time, then use append afterwards to add to it.
with open(filename, "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(quotes)

# To delete the csv file afterwards
#os.remove("quote_list.csv")
import requests
from bs4 import BeautifulSoup
import csv
# Delete later: import tabulate

# Enter the URL of the site you are scraping
URL="https://quotes.toscrape.com/"
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
    quote["lines"] = x.find("span", attrs={"class": "text"}).string
    quote["author"] = x.find("small", attrs={"class": "author"}).string
    print(num, ": ", quote["lines"], " by ", quote["author"])
    quotes.append(quote)
    num +=1

# Just for checking, delete later
# header = quotes[0].keys()
# rows =  [x.values() for x in quotes]
# print(tabulate.tabulate(rows, header))

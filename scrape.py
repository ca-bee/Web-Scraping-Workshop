import requests
from bs4 import BeautifulSoup

# Enter the URL of the site you are scraping
URL=""
r=requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')
# To get a better formatted visual representation:
# print(soup.prettify)


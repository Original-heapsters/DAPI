import bs4
from requests_html import HTMLSession
# create an HTML Session object
session = HTMLSession()
# Use the object above to connect to needed webpage
resp = session.get("https://monkishbrewing.square.site/")
# Run JavaScript code on webpage
resp.html.render()
soup = bs4.BeautifulSoup(resp.html.html, 'html.parser')
# print(soup.prettify())
byClass = soup.find_all("div", class_="w-wrapper fluid-carousel--item carousel-item--medium")
print(byClass)

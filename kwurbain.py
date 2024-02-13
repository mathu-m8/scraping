import requests
from bs4 import BeautifulSoup
import http.cookiejar

url = "https://www.kwurbain.ca/inscriptions"

session = requests.Session()
session.cookies = http.cookiejar.LWPCookieJar(filename="cookies.txt")

response = session.get(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"})

if response.status_code == 200:
    print("Cookies received successfully.")
else:
    print(f"Failed to get cookies. Status code: {response.status_code}. Exiting.")
    exit()

soup = BeautifulSoup(response.content, "html.parser")
# AGENCY LISTINGS
agency_list = soup.select(".card.property-card.mix")
agencies = []
for agency in agency_list:
    property_title = agency.find("h5").text.strip()
    property_price = agency.find("span").text.strip()
    agencies.append({'title': property_title, 'price': property_price})
    # print(f"Title: {property_title}")
    # print(f"Price: {property_price}")
print(agencies)
# print(agencies[0]['title'])
session.cookies.save(ignore_discard=True)

session.close()

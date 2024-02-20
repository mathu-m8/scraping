import http.cookiejar

import requests
from bs4 import BeautifulSoup


def get_cookies_and_soup(url):
    session = requests.Session()
    session.cookies = http.cookiejar.LWPCookieJar(filename="../cookies.txt")

    response = session.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"})

    if response.status_code == 200:
        print("Cookies received successfully.")
    else:
        print(f"Failed to get cookies. Status code: {response.status_code}. Exiting.")
        exit()

    soup = BeautifulSoup(response.content, "html.parser")

    return session, soup

from helper_functions import get_cookies_and_soup


def extract_commercial_data(soup):
    commercial_list = soup.select(".card.property-card.mix")
    commercials = []
    for commercial in commercial_list:
        property_title = commercial.find("h5").text.strip()
        property_price = commercial.find("span").text.strip()
        commercials.append({'title': property_title, 'price': property_price})
    return commercials


def main():
    # FEATURED COMMERCIAL PROPERTIES
    agency_url = "https://www.kwurbain.ca/inscriptions/commercial/"
    session, soup = get_cookies_and_soup(agency_url)
    commercials = extract_commercial_data(soup)
    print(commercials)
    print(f"Total Commercials: ", len(commercials))
    session.cookies.save(ignore_discard=True)
    session.close()


if __name__ == "__main__":
    main()

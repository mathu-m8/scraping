from helper_functions import get_cookies_and_soup


def extract_agency_data(soup):
    agency_list = soup.select(".card.property-card.mix")
    agencies = []
    for agency in agency_list:
        property_title = agency.find("h5").text.strip()
        property_price = agency.find("span").text.strip()
        agencies.append({'title': property_title, 'price': property_price})
    return agencies


def main():
    # AGENCY LISTINGS
    agency_url = "https://www.kwurbain.ca/inscriptions"
    session, soup = get_cookies_and_soup(agency_url)
    agencies = extract_agency_data(soup)
    print(agencies)
    print(f"Total Agencies: ", len(agencies))
    session.cookies.save(ignore_discard=True)
    session.close()


if __name__ == "__main__":
    main()

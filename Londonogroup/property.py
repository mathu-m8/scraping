from helper_functions import get_cookies_and_soup


def extract_agency_data(soup):
    global property_type, property_value
    properties_list = soup.select(".project-item")

    properties = []
    for property in properties_list:
        property_titles = property.select('.title')
        property_desc = property.select_one(".desc").get_text(strip=True)
        first_title_text = property_titles[0].get_text(strip=True)
        second_title_text = property_titles[1].get_text(strip=True)

        if "Sale" in first_title_text:
            property_type = 'Sale'
            property_value = first_title_text.split(":")[1]
        if "Rent" in second_title_text:
            property_type = 'Rent'
            property_value = second_title_text.split(":")[1]

        properties.append({'type': property_type, 'value': property_value, 'description': property_desc})
    return properties


def main():
    # AGENCY LISTINGS
    url = "https://www.londonogroup.com/property/search.php"
    session, soup = get_cookies_and_soup(url)
    properties = extract_agency_data(soup)
    print(properties)
    print(f"Total Agencies: ", len(properties))
    session.cookies.save(ignore_discard=True)
    session.close()


if __name__ == "__main__":
    main()

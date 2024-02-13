from helper_functions import get_cookies_and_soup


def extract_luxury_data(soup):
    luxury_list = soup.select(".card.property-card.mix")
    luxuries = []
    for luxury in luxury_list:
        property_title = luxury.find("h5").text.strip()
        property_price = luxury.find("span").text.strip()
        property_address = luxury.find("h6").text.strip().replace('\r\n', '').strip()

        icons_container = luxury.select_one(".card-icons")

        bath = icons_container.select_one('.icon')
        bed = bath.find_next('div')
        bath_count = bath.text.strip()
        bed_count = bed.text.strip()

        luxuries.append({
            'title': property_title,
            'price': property_price,
            'address': ' '.join(property_address.split()),
            'bath': bath_count,
            'bed': bed_count
        })
    return luxuries


def main():
    # FEATURED LUXURY PROPERTIES
    url = "https://www.kwurbain.ca/inscriptions/luxe/"
    session, soup = get_cookies_and_soup(url)
    luxuries = extract_luxury_data(soup)
    print(luxuries)
    # print(f"Total luxuries: ", len(luxuries))
    session.cookies.save(ignore_discard=True)
    session.close()


if __name__ == "__main__":
    main()

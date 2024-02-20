import json

from helper_functions import get_cookies_and_soup


def main():
    url = "https://joellebitar.com/inscriptions/"
    session, soup = get_cookies_and_soup(url)
    properties = soup.select(".mix.all")
    commerciales = []
    for property_element in properties:
        image_url = property_element.select_one('img.lazyload').get('data-src')
        property_detail = property_element.select_one('h4').text.strip()
        property_name = property_element.select_one('h6').text.strip()
        price = property_element.select_one(".col-lg-4.col-sm-6.col-xs-12.text-xs-center").find('h6').text.strip()
        bed_count = property_element.select_one('.list-inline-item:nth-child(1)').text.strip()
        shower_count = property_element.select_one('.list-inline-item:nth-child(2)').text.strip()
        property_url = property_element.select_one('a').get('href')
        com_property = {
            "image_url": image_url,
            "property_name": property_name,
            "price": price,
            "bed_count": bed_count,
            "shower_count": shower_count,
            "property_detail": property_detail,
            "property_url": property_url
        }
        commerciales.append(com_property)
    json_commerciales_properties = json.dumps(commerciales, indent=2)
    with open('commerciales.json', 'w') as json_file:
        json_file.write(json_commerciales_properties)


if __name__ == "__main__":
    main()

import requests
import bs4
import json

JSON = 'cars.json'
HOST = 'https://av.by/'
URL = 'https://moto.av.by/filter?category_type=1'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
}


def get_html(url, params=''):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_content(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='listing-item__wrap')
    cards = []
    for item in items:
        cards.append(
            dict(title_car=item.find('span', class_='link-text').text,
                 href_car=item.find('a', class_='listing-item__link').get('href'),
                 price_car_byn=item.find('div', class_='listing-item__price').text.encode('ascii', errors='ignore').decode('UTF-8'),
                 price_car_usd=item.find('div', class_='listing-item__priceusd').text.replace('\xa0', ' '))
        )

    print(cards)

    return cards


def parser():
    PAGENATION = int(input('Pages: '))
    html = get_html(URL)
    if html.status_code == 200:
        cads = []

        for page in range(1, PAGENATION + 1):
            print(f'Parsing {page}')
            html = get_html(URL, params='&page=' + str(page + 1))
            cads.extend(get_content(html.text))
    else:
        print("Error")


parser()

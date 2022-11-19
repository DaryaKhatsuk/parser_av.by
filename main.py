import csv
import json

import bs4
import requests

JSON = 'cars.json'
CSV = 'cars.csv'
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
        try:
            title_car = item.find('span', class_='link-text').text
            href_car = ['https://moto.av.by' + item.find('a', class_='listing-item__link').get('href')]
            price_car_byn = item.find('div', class_='listing-item__price').text.replace('\xa0', ' ').replace(
                '\u2009', ' ')
            price_car_usd = item.find('div', class_='listing-item__priceusd').text.replace('\xa0', ' ').replace(
                '\u2009', ' ')
            message_car = item.findNext('div', class_='listing-item__message').text.replace('\n', ' ') \
                .replace('\\', '/').replace('\xa0', ' ')
            card = {'title_car': title_car, 'href_car': href_car, 'price_car_byn': price_car_byn,
                    'price_car_usd': price_car_usd, 'message_car': message_car}
            cards.append(card)
        except Exception as ex:
            print(f'Some {ex} here')

    return cards


def safe_doc(items, path):
    with open(path, 'w', newline='', encoding='UTF-8') as file:
        sl = {}
        sc = 1

        for item in items:
            with open('cars.csv', 'a+', newline='', encoding='UTF=8') as csvfile:
                csvF = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
                csvF.writerow(item.values())
            sl.update(
                {
                    "title_car " + str(sc): item["title_car"],
                    "href_car " + str(sc): item["href_car"],
                    "price_car_byn " + str(sc): item["price_car_byn"],
                    "price_car_usd " + str(sc): item["price_car_usd"],
                    "message_car " + str(sc): item["message_car"],
                }
            )
            sc += 1
        json.dump(sl, file, indent=4, ensure_ascii=False)


def parser():
    PAGENATION = int(input('Pages: '))
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION + 1):
            print(f'Parsing {page}')
            html = get_html(URL, params='&page=' + str(page + 1))
            cards.extend(get_content(html.text))
        safe_doc(cards, JSON)
    else:
        print("Error")


parser()

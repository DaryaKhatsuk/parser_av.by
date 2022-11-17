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
            {
                # 'img_car': item.find('img', class_=' ls-is-cached lazyloaded').get_text(),
                'title_car': item.find('span', class_='link-text').get_text(),
                'href_car': item.find('a', class_='listing-item__link').get_text(),
                'price_car': item.findNext('div', class_='listing-item__price'),

            }
        )
        print(cards)

    return cards


def parser():
    PAGENATION = int(input('Pages: '))
    html = get_html(URL)
    if html.status_code == 200:
        cads = []
        for page in range(1, PAGENATION +1):
            print(f'Parsing {page}')
            html = get_html(URL, params='%page=' + str(page + 1))
            cads.extend(get_content(html.text))
        # print(cads)
    else:
        print("Error")


parser()


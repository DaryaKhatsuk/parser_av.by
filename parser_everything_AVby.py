import requests
from bs4 import BeautifulSoup

HOST = 'https://av.by/'
URL = 'https://cars.av.by/filter?brands'


def get_html(url):
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/108.0.0.0 '
                      'Safari/537.36',
    }
    req = requests.get(url, headers=HEADERS)
    return req


def parse(html):
    # Примерное максимальное количество страниц которое я смогла обнаружить для одной модели в принципе
    count_s = 120
    brand = 0
    # Здесь не все модели, так что остальные программа будет пропускать
    br = {'AlfaRomeo', 'Dodge', 'Kia', 'Nissan', 'Skoda', 'Audi', 'Fiat', 'Lada(ВАЗ)', 'Opel', 'Subaru', 'BMW',
          'Ford', 'Lexus', 'Peugeot', 'Suzuki', 'Chevrolet', 'Geely', 'Mazda', 'Renault', 'Toyota', 'Chrysler', 'Honda',
          'Mercedes-Benz', 'Rover', 'Volkswagen', 'Citroen', 'Hyundai', 'Mitsubishi', 'SEAT', 'Volvo'}
    br_len = len(br)
    control = 1
    # Если программа нашла меньше моделей, чем в сете, то цикл будет продолжатся
    while control <= br_len:
        sum_list = []
        brand += 1
        # Объект супа ищущий действительную строку с моделями
        soup = BeautifulSoup(get_html(html + f'[0][brand]={brand}').text, 'html.parser')
        # если страница с моделью существует и отдает 200, идем дальше
        if get_html(html + f'[0][brand]={brand}').status_code == 200:
            soup_find = soup.find('span', class_='dropdown-floatlabel__value').text.replace(' ', '')
            # Сравнивает полученное название с объектами сета
            if soup_find in br:
                control += 1
                print(f'№{control}\n-{soup_find}-')
                for i in range(1, count_s + 1):
                    # Создаем суп из страницы, находим все цены и поочередно добавляем в список.
                    # Повторяем пока страницы не кончатся
                    soup = BeautifulSoup(get_html(html + f'[0][brand]={brand}&page={i}').text, 'html.parser')
                    lict_new = soup.findAll('div', class_='listing-item__wrap')
                    for j in lict_new:
                        sum_list.append(int(j.find('div', class_='listing-item__price').text.replace('\xa0р.', '')
                                            .replace('\u2009', '')))
                else:
                    # вывод результата
                    sum_all = sum(sum_list)
                    resp = sum_all // len(sum_list)
                    print('Средняя цена', resp)
                    print('Максимальная цена', max(sum_list))
                    print('Минимальная цена', min(sum_list))
            else:
                # Если поймали то, что не нужно, отпускаем и движемся дальше
                continue
        else:
            # Если страница отсутствует, происходит else и движемся дальше
            continue
    else:
        print('finish')


parse(URL)

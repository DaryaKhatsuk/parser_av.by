import asyncio
import lxml
import csv
import json
import time
import re
import aiohttp
from bs4 import BeautifulSoup


class ParserAV:
    def __init__(self):
        """
        :self.JSON, self.CSV: переменные содержащие названия файлов в проекте форматов .json и .csv.
        :self.HOST: host сайта.
        :self.URL: url раздела, в котором производится парсинг.
        :self.HEADERS: искать в главном домене раздела "сеть"/"network" консоли браузера.
        """
        self.JSON = 'cars.json'
        self.CSV = 'cars.csv'
        self.HOST = 'https://av.by/'
        self.URL = 'https://moto.av.by/filter?category_type=1'
        self.HEADERS = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
        }
        self.cards = []
        self.count = 0

    async def get_content(self, session_request, mess):
        """
        :param session_request: получает всю html информацию со страницы от функции parser.
        :soup: берет данный со страницы отправленные функцией parser
        :items: собирает со всей страницы все div классы под названием listing-item__wrap
        :AttributeError: обрабатывает отсутствие в карточках описания, т.к. это необязательный для
         заполнения пользователем параметр.
        :Exception: общее исключение для обработки внезапных ошибок.
        :return: safe_doc(cards), передает данные для сохранения в форматах json и csv
        """
        bike_rus = {'АВМ', 'Альфамото', 'Восход', 'Днепр', 'ЗиД', 'ИЖ', 'Минск', 'Урал', 'Эксклюзив'}
        moto_rus = {
            'АВМ': 'avm',
            'Альфамото': 'alfamoto',
            'Восход': 'voshod',
            'Днепр': 'dnepr',
            'ЗиД': 'zid',
            'ИЖ': 'izh',
            'Минск': 'minsk',
            'Урал': 'ural',
            'Эксклюзив': 'eksklyuziv',
        }
        if mess in bike_rus:
            mess = moto_rus.get(mess)
        # mess = str(mess).lower()
        soup = BeautifulSoup(await session_request, 'html.parser')
        items = soup.find_all('div', class_='listing-item__wrap')
        # items_top = soup.find_all('div', class_='listing-item__wrap')
        # print(items)
        for item in items:
            # print(items)
            try:
                title_car = item.find('span', class_='link-text').text
                print(title_car)
                if re.findall(pattern='(^)' + f'{mess}' + '+.{,22}', string=str(title_car)):
                    href_car = 'https://moto.av.by' + item.find('a', class_='listing-item__link').get('href')
                    price_car_byn = item.find('div', class_='listing-item__price').text.replace('\xa0', ' ') \
                        .replace('\u2009', ' ')
                    price_car_usd = item.find('div', class_='listing-item__priceusd').text.replace('\xa0', ' ') \
                        .replace('\u2009', ' ').replace('≈', ' ')
                    params_car = item.findNext('div', class_='listing-item__params').text.replace('\n', ' ') \
                        .replace('\u2009', ' ').replace('\xa0', ' ')
                    print(f"{title_car}\nСсылка: {str(href_car)}\n"
                          f"Характеристики: {params_car}\n"
                          f"Цена в BYN: {price_car_byn}\n"
                          f"Цена в USD:{price_car_usd.replace('≈', ' ')}")
                    self.count += 1
                # title_car = item.find('a', class_='catalog__link').text
                # href_car = 'https://moto.av.by' + item.find('a', class_='listing-item__link').get('href')
                # price_car_byn = item.find('div', class_='listing-item__price').text.replace('\xa0', ' ').replace(
                #     '\u2009', ' ')
                # price_car_usd = item.find('div', class_='listing-item__priceusd').text.replace('\xa0', ' ').replace(
                #     '\u2009', ' ')
                # message_car = item.findNext('div', class_='listing-item__message').text.replace('\n', ' ') \
                #     .replace('\\', '/').replace('\xa0', ' ')
                # card = {'title_car': title_car, 'href_car': href_car, 'price_car_byn': price_car_byn,
                #         'price_car_usd': price_car_usd, 'message_car': message_car}
                # print(title_car)
                # self.cards.append(title_car)
            # except AttributeError:
            #     title_car = item.find('span', class_='link-text').text
            #     href_car = ['https://moto.av.by' + item.find('a', class_='listing-item__link').get('href')]
            #     price_car_byn = item.find('div', class_='listing-item__price').text.replace('\xa0', ' ').replace(
            #         '\u2009', ' ')
            #     price_car_usd = item.find('div', class_='listing-item__priceusd').text.replace('\xa0', ' ').replace(
            #         '\u2009', ' ')
            #     card = {'title_car': title_car, 'href_car': href_car, 'price_car_byn': price_car_byn,
            #             'price_car_usd': price_car_usd, 'message_car': 'Pass'}
            #     self.cards.append(card)
            #     print(f'message_car: pass')
            except Exception as ex:
                print(f'Some {ex} here.')

    # def safe_doc(self):
    #     """
    #     :return: запись в json и csv файлы.
    #     """
    #     with open(self.JSON, 'w', newline='', encoding='UTF-8') as file:
    #         sl = {}
    #         sc = 1
    #         for item in self.cards:
    #             sl.update(
    #                 {
    #                     "title_car " + str(sc): item["title_car"],
    #                 }
    #             )
    #             sc += 1
    #         json.dump(sl, file, indent=4, ensure_ascii=False)
    #         print('The data is saved in JSON.')
    #     with open(self.CSV, 'w', newline='', encoding='UTF=8') as csvfile:
    #         for item in self.cards:
    #             csvF = csv.writer(csvfile, delimiter=',', quotechar=' ', quoting=csv.QUOTE_ALL)
    #             csvF.writerow(item.values())
    #         print('The data is saved in CSV.')

    async def parser(self):
        """
        :async with aiohttp.ClientSession(): позволяет использовать одну сессию несколько раз.
        :session_request (первый): использует данные url и headers сети.
        :session_request.status == 200: проверяет что бы статус подключения на странице был 200,
         т.е. существующей, не пустой страницей.
        :counter: является счетчиком для отсчитывания страниц, в виду использования цикла while
        :session_request (второй): подставляет в открытую сессию точные данные страницы, которую нужно спарсить сейчас.
        :asyncio.create_task(get_content(session_request.text())): создает асинхронную задачу передачи данных со
         страницы, в виде текста, в функцию get_content.
        """
        async with aiohttp.ClientSession() as session:
            session_request = await session.get(url=self.URL, headers=self.HEADERS)
            counter = 1
            while session_request.status == 200:
                session_request = await session.get(url=self.URL + '&page=' + str(counter))
                print(f'Parsing page {counter}')
                asyncio.create_task(self.get_content(session_request.text(), 'Apollo'))
                counter += 1
            # else:
                # print(f"Session status: {session_request.status}. Data is being saved.")
                # self.safe_doc()

    def par(self):
        x = time.time()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait([self.parser()]))
        y = time.time()
        print(y - x)
        print(self.count)


parser_run = ParserAV()
parser_run.par()

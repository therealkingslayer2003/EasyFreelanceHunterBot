import requests
from bs4 import BeautifulSoup
import lxml


def get_orders():
    url = 'https://kwork.ru/projects?fc=41&attr=211'
    query = requests.get(url)

    soup = BeautifulSoup(query.text, 'lxml')

    orders = soup.findAll('div', class_='card__content pb5')

    #title_and_prices = []

    for order in orders:
        order_title = order.find('div', class_='mb15').find('div', class_='d-flex relative'). \
            find('div', class_='wants-card__left').find('div',
                                                        class_='wants-card__header-title first-letter breakwords pr250'). \
            find('a').text.strip()
        order_price = order.find('div', class_='mb15').find('div', class_='d-flex relative').find('div', class_='wants-card__header-right-block').find('div', class_='wants-card__header-controls projects-list__icons'). \
            find('div', class_='wants-card__header-price wants-card__price m-hidden').text.strip()
        print(f'{order_title} , {order_price}\n')


get_orders()

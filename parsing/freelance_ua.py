from selenium.webdriver import Chrome
#from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

browser = Chrome(executable_path='chromedriver.exe')

#Selenuim
url = 'https://freelance.ua/orders/'
browser.get(url)

#Parsing

all_orders = []

for i in range(4):
    html_page = BeautifulSoup(browser.page_source, 'lxml')

    orders = html_page.findAll('li', class_='j-order')

    for order in orders:
        title = order.find('header', class_='l-project-title').find('a').text
        link = order.find('header', class_='l-project-title').find('a').get('href')
        description = order.find('article').find('p').text
        answers = order.find('ul', class_='l-item-features').findAll('li')[-1].find('a').find('span').text
        all_orders.append([title, answers, link, description])
        #"next" button
        next_button = browser.find_element_by_xpath('//*[@id="j-orders-search-list"]/div[6]/ul/li[7]/a')
        next_button.click()

print(all_orders)
print(len(all_orders))
#!/home/dmitriy/anaconda3/bin/python
import requests
import urllib.parse
from bs4 import BeautifulSoup
from collections import namedtuple

InnerBlock = namedtuple ('Block', 'title, price, url')

class Block(InnerBlock):

    def __str__(self):
        return f'{self.title}\t{self.price}\t{self.url}'

class AutoParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
                'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
                'Accept-Language': 'ru',
                }
    def get_page(self, page: int = None):
        params = {}

        if page and page > 1:
            params['page'] = page

        url = 'https://auto.ru/ivanovo/cars/hyundai/solaris/all/'
        r = self.session.get(url, params=params)
        r.encoding = 'utf-8'
        return r.text
    
    def parse_date():
        pass
    
    def get_pagination_limit(self):
        text = self.get_page()
        soup = BeautifulSoup(text, 'lxml')
        container = soup.select("a.Button.Button_color_whiteHoverBlue.Button_size_s.Button_type_link.Button_width_default.ListingPagination-module__page")
        last_button = container[-1]
        href = last_button.get('href')
        r = urllib.parse.urlparse(href)
        r = urllib.parse.parse_qs(r.query)
        return int(r['page'][0])

    def get_blocks(self, page: int = None):
        text = self.get_page(page = page)
        soup = BeautifulSoup(text, 'lxml')
        container = soup.select("div.ListingItem-module__main")
        for item in container:
            block = self.parse_block(item = item)
            #print(block)

    def parse_block(self, item):
        url_block = item.select_one('a.Link.ListingItemTitle-module__link')
        #Марка Машины
        title_block = url_block.get_text('\n')
        title = title_block.strip()
        #Стоимость 
        price_block = item.find(class_='ListingItemPrice-module__content')
        if price_block:
            price = price_block
        else:
            price = BeautifulSoup('<span>Автомобиль продан</span', 'lxml')
        price = price.get_text('\n')
        price = list(map(lambda i: i.replace(u'\xa0', ' ').replace('от ', '' ), price.split('\n')))
        #Дата
        #Ссылка на объявление
        href = url_block.get('href')
        if href:
            url = href
        else:
            url = None
        return Block(
                url = url,
                title = title,
                price = price,
                )
        
    def parse_all(self):
        limit = self.get_pagination_limit()
        print ('Всего страниц %s' % (limit))
        for i in range (1, limit + 1):
            self.get_blocks(page = i)

def main():
    p = AutoParser()
    p.parse_all()

if __name__ == '__main__':
    main()

import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver


class Scraper:

    def __init__(self, test):
        self.test = test
        n, u, p = self.walmart(test)
        n1, u1, p1 = self.ebay(test)
        n.extend(n1)
        u.extend(u1)
        p.extend(p1)

        self.make_df(n, p, u)

    def make_df(self, title, price, url):

        """
        this function make a data frame using pandas

        :param title: a list of products title [list]
        :param price: title: a list of products prices [list]
        :param url: title: a list of products urls [list]
        :return: output first 5 rows in the data frame
        """

        print(len(title), len(price), len(url))
        data = {
            'title': title,
            'price': price,
            'url': url
        }
        df = pd.DataFrame(data)
        print(df.head())

    def walmart(self, test_w):

        """
        this scrap's through walmart store

        :param test_w: the search term
        :return: a lists of prises, titles and urls of products in walmart
        """

        name = []
        price = []
        url = []

        driver = webdriver.Chrome()
        driver.get('https://www.walmart.com/')
        search_bar = driver.find_element_by_id('global-search-input')
        search_bar.send_keys(test_w)
        search_bar.send_keys(Keys.RETURN)

        time.sleep(5)
        u = driver.current_url
        driver.quit()

        source = requests.get(str(u)).text
        soup = BeautifulSoup(source, 'lxml')

        l_n = soup.findAll('a', {'class': 'product-title-link line-clamp line-clamp-2 truncate-title'})
        values = soup.findAll('span', {'class': 'price display-inline-block arrange-fit price price-main'})

        for value in values:
            price_s = value.find('span')
            price.append(price_s.text)

        for i in l_n:
            name_s = i.find('span')
            url.append('https://www.walmart.com' + i.attrs['href'])
            name.append(name_s.text)

        # loops through lists to check if there's any uncompleted values
        if len(price) != len(url) != len(name):
            while len(price) != len(url) != len(name):
                if len(price) > len(url):
                    price.pop()
                elif len(url) > len(name):
                    url.pop()
                elif len(name) > len(price):
                    name.pop()
        return name, url, price

    def ebay(self, test_e):
        name = []
        price = []
        url = []

        driver = webdriver.Chrome()
        driver.get('https://www.ebay.com/')
        search_bar = driver.find_element_by_id('gh-ac')
        search_bar.send_keys(test_e)
        search_bar.send_keys(Keys.RETURN)

        WebDriverWait(driver, 6)
        u = driver.current_url
        driver.quit()

        source = requests.get(str(u)).text
        soup = BeautifulSoup(source, 'lxml')

        links = soup.findAll('a', {'class': 's-item__link'})
        titles = soup.findAll('h3', {'class': 's-item__title'})
        values = soup.findAll('span', {'class': 's-item__price'})

        for link in links:
            url.append(link.attrs['href'])
        for title in titles:
            name.append(title.text)
        for value in values:
            price.append(value.text)

        if len(price) != len(url) != len(name):
            while len(price) != len(url) != len(name):
                if len(price) > len(url):
                    price.pop()
                elif len(url) > len(name):
                    url.pop()
                elif len(name) > len(price):
                    name.pop()
        return name, url, price


if __name__ == "__main__":
    Scraper('SEARCH HERE')

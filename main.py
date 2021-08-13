# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://auto.ru/cars/used/?page={}'


def get_soup_object(url):
    try:
        page = requests.get(url)
        if page.status_code == 200:
            page = page.content.decode('utf-8')
            soup = BeautifulSoup(page, 'lxml')
            return soup
    except Exception as e:
        print(e)


def get_pages_count(soup):
    pages = soup.find_all('span', class_='Button__text')
    return int(pages[-4].text)


def collect_all_links(soup):
    links = soup.find_all('a', class_='Link ListingItemTitle__link')
    finish_links = [link['href'] for link in links]
    return finish_links


if __name__ == '__main__':
    soup = get_soup_object(BASE_URL.format(1))
    links = collect_all_links(soup)
    print(collect_all_links(soup))

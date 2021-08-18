# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from init_logger import init_logger

logger = init_logger('logger')

BASE_URL = 'https://auto.ru/cars/used/?page={}'


def get_soup_object(url):
    try:
        page = requests.get(url)
        if page.status_code == 200:
            page = page.content.decode('utf-8')
            soup = BeautifulSoup(page, 'lxml')
            return soup
    except Exception as e:
        logger.error(e)


def get_pages_count(soup):
    pages = soup.find_all('span', class_='Button__text')
    return int(pages[-4].text)


def collect_all_links(soup):
    attempt = 0
    while attempt < 5:
        try:
            links = soup.find_all('a', class_='Link ListingItemTitle__link')
            finish_links = [link['href'] for link in links]
            return finish_links
        except Exception as e:
            logger.error(f"Error while collect all links from page: {e}")
        attempt += 1


def str_to_int(str):
    str = ''.join([c for c in str if c.isdigit()])
    return int(str)


def parse_info_from_one_car(url, cars):
    soup = get_soup_object(url)
    mark = soup.find('h1', class_='CardHead__title').text

    if soup.find("div", {"class": "CardSold__title"}):
        return
    price = str_to_int(soup.find("span", {"class": "OfferPriceCaption__price"}).text)
    year_of_release = soup.find("a", {"class": "Link Link_color_black"}).text
    mileage = str_to_int(soup.find("li", {"class": "CardInfoRow CardInfoRow_kmAge"}).text)
    body_type = soup.find("li", {"class": "CardInfoRow CardInfoRow_bodytype"}).text[5:]
    cars.append({
        "mark": mark,
        "link": url,
        "info": {
            "price": price,
            "year_of_release": year_of_release,
            "mileage": mileage,
            "body type": body_type
        }
    })


if __name__ == '__main__':
    soup = get_soup_object(BASE_URL.format(1))
    pages = get_pages_count(soup)  # collect all pages from http://auto.ru
    cars = []
    for page in tqdm(range(1, pages)):
        logger.info(f"Parsing page {page} of {pages}")
        links = collect_all_links(soup)  # this function collect all links from page http:://auto.ru
        for link in links:
            parse_info_from_one_car(link, cars)
    print(cars)

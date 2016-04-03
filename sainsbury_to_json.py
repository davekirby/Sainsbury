#! /usr/bin/env python2

''' Read Sainsbury product web pages and write as JSON to stdout
'''

from __future__ import print_function
from bs4 import BeautifulSoup
import re
import requests
from pprint import pprint

import sys

DEFAULT_URL = 'http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/5_products.html'
PRICE_REGEX = re.compile(r'([\d\.]+)')


def parse_products(html):
    doc = BeautifulSoup(html, 'html.parser')
    results = []
    for product_div in doc.find_all('div', class_='product'):
        result = {}
        anchor = product_div.find('h3').a
        result['url'] = anchor['href']
        result['title'] = anchor.text.strip()
        price_text = product_div.find('p', class_='pricePerUnit').text
        price = float(PRICE_REGEX.search(price_text).group(1))
        result['unit_price'] = price
        results.append(result)
    return results


def parse_single_product(html):
    doc = BeautifulSoup(html, 'html.parser')
    h3 = doc.find('h3', text='Description')
    description = h3.find_next_sibling('div').text.strip()
    return description


def size_to_kb(size):
    ''' convert a file size in bytes to a string with kilobytes
    N.B. assumes that 1kb = 1024 bytes.  YMMV
    '''
    return "{:.3}kb".format(size/1024.0)

def convert_web_to_json(url):
    ''' Retrieve web pages with product information and convert to JSON '''
    response = requests.get(url)
    results = []
    total = 0
    if 200 <= response.status_code <= 299:
        products = parse_products(response.text)
        for product in products:
            result = {'title' : product['title'],
                      'unit_price' : product['unit_price'] }

            product_page_response = requests.get(product['url'])
            if 200 <= product_page_response.status_code <= 299:
                result['size'] = size_to_kb(len(product_page_response.content))
                result['description'] = parse_single_product(product_page_response.text)
            else:
                raise Exception("Error: HTTP status {} when trying to retrieve page {}".format(
                    product_page_response.status_code, product['url']))

            total += product['unit_price']
            results.append(result)
        return {'results' : results, 'total' : total}

    else:
        raise Exception("Error: HTTP status {} when trying to retrieve page {}".format(response.status_code, url))


if __name__ == '__main__':
    if len(sys.argv) > 3 or sys.argv[-1] in ['-h', '--help']:
        print(
'''Usage: {} [url]
Download web page at URL and its child pages, and convert to JSON.
url defaults to {} if not specified.
''').format(sys.argv[0], DEFAULT_URL)
        sys.exit(0)

    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
        url = DEFAULT_URL

    json = convert_web_to_json(url)
    pprint(json)
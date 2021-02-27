import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path

path = Path("./midwayusa.txt")
file = open("./midwayusa.txt", "r")
web_urls = file.read()
file.close()
urls = web_urls.split('\n')


def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    for data in soup.find_all('meta'):
        if data.get('property') == "og:title":
            title = data.get("content")
        if data.get('property') == "og:url":
            supplier = data.get("content")
        if data.get('property') == "og:site_name":
            product_link = data.get("content")
    stock_status = soup.find(
        'span', {'ng-bind': 'selector.productAvailability'}).getText()

    if stock_status == 'Mixed Availability':
        stock_status = 'Variant'
    elif stock_status == 'Available':
        stock_status = 'In Stock'

    return title, supplier, product_link, stock_status


with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for url in urls:
        title, supplier, product_link, stock_status = get_data(url)
        writer.writerow([title, supplier, product_link, stock_status])
file.close()

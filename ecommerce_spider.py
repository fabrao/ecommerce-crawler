import lxml.html as parser
import requests
import csv
from urllib.parse import urlsplit, urljoin


class EcommerceSpider(object):
    def __init__(self, start_url):
        self.links = set()
        self.items = []
        self.start_url = start_url
        self.set_base_url()

    def crawl(self):
        self.get_links()
        self.get_items()

    def crawl_to_file(self, filename):
        self.crawl()
        self.save_items(filename)

    def get_links(self):
        r = requests.get(self.start_url)
        html = parser.fromstring(r.text)

        item_url_xpath = "//a[@class='card-product-url']/@href"
        next_page_xpath = "//div[@class='card card-pagination']/ul/li/a/@href"
        self.parse_links(html, item_url_xpath)

        next_page = html.xpath(next_page_xpath)[9]
        print ("NEXT_PAGE-PRIMEIRO: %s" % next_page)

        while next_page:
            r = requests.get(urljoin(self.base_url, next_page))
            html = parser.fromstring(r.text)
            self.parse_links(html, item_url_xpath)

            try:
                print ("\n NEXT_PAGE-ANTES: %s" % next_page)
                #print ("\n next_page_xpath-antes: %s" % next_page_xpath) #//div[@class='card card-pagination']/ul/li/a/@href
                next_page = html.xpath(next_page_xpath)[9]
                print ("\n NEXT_PAGE-DEPOIS: %s" % next_page)

            except IndexError as e:
                next_page = None

    def get_items(self):
        for link in self.links:
            r = requests.get(link)
            html = parser.fromstring(r.text)
            self.items.append(self.extract_item(html, link))

    def extract_item(self, html, link):
        try:
            name = html.xpath("//h1[@class='product-name']/text()")[0]
        except IndexError as e:
            print ("Name not found at page %s" % link)
            name = "Not found"

        try:
            price_str = html.xpath("//p[@class='sales-price']/text()")[0]
            price = float(price_str[3:].replace(".", "").replace(",", "."))
            print ("TRACE: extract_item: try 2")
        except IndexError as e:
            print("Price not found at page %s" % link)
            price = "Not found"

        return {
            'url': link,
            'name': name,
            'price': price
        }

    def parse_links(self, html, item_url_xpath):
        new_links = html.xpath(item_url_xpath)
        new_links = [self.prepare_url(l) for l in new_links]
        self.links = self.links.union(set(new_links))

    def set_base_url(self):
        self.base_url = urlsplit(self.start_url)._replace(path="", query="").geturl()

    def prepare_url(self, url):
        url = urljoin(self.base_url, url)
        return urlsplit(url)._replace(query="").geturl()

    def save_items(self, filename):
        keys = self.items[0].keys()
        with open(filename, 'w') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


spider = EcommerceSpider("https://www.submarino.com.br/categoria/celulares-e-smartphones/smartphone/f/preco-500.0:9000.0")
#spider.crawl_to_file("motog.csv")
spider.crawl()
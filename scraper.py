import scrapy


class BrickSetSpider(scrapy.Spider):
    name = 'brick_spider'
    start_urls = ['https://www.americanas.com.br/categoria/celulares-e-smartphones/smartphone']

    def parse(self, response):
        SET_SELECTOR = '.product-grid-item'
        for brickset in response.css(SET_SELECTOR):

            PRODUCT_NAME_SELECTOR = 'a ::name'
            PRODUCT_LINK_SELECTOR = 'a ::href'
            #NAME_SELECTOR = 'h1 a ::text'
            #PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            #MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            #IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'NOME': brickset.css(PRODUCT_NAME_SELECTOR).extract_first()
            #    'LINK': brickset.css(PRODUCT_LINK_SELECTOR).extract_first()
            #    'Product': brickset.css(NAME_SELECTOR).getall(),
            #    'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
            #    'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
            #    'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }

        #NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        #next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        #if next_page:
        #    yield scrapy.Request(
        #        response.urljoin(next_page),
        #        callback=self.parse
        #    )
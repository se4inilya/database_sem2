import scrapy


class zvetsad(scrapy.Spider):
    name = "zvetsad"

    start_urls = [
        'https://www.zvetsad.com.ua/catalog/angliyskie-rozyi-david-austin'
    ]
    allowed_domains = [
        'zvetsad.com.ua'
    ]

    def parse(self, response):
        for product in response.xpath('//div[@class="product-card"]'):
            price = product.xpath(
                './/div[@class="product-card__actions"]/div[@class="product-card__prices"]/text()').get()
            price = price.replace(' ', ' ')
            yield {
                'link': product.xpath(
                    './/div[@class="product-card__info"]/div[@class="product-card__name"]/a/@href').extract(),
                'price': price.strip(),
                'img': product.xpath('.//div[@class="product-card__image product-image"]/a/img/@src').extract(),
                'name': product.xpath(
                    './/div[@class="product-card__info"]/div[@class="product-card__name"]/a/text()').get()
            }

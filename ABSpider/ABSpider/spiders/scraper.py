import scrapy

class ABspiderSpider(scrapy.Spider):
    name = 'scraper'
    allowed_domains = ['abcam.com']
    start_urls = ['https://www.abcam.com/en-nl/products/primary-antibodies']
    main = 'https://www.abcam.com'

    def parse(self, response):
        products = response.css('div.pb-4')
        
        for product in products:
            item = {
                'name': product.css('a::text').get(),
                'id': product.css('p.font-bold::text').get(),
                'url': self.main + product.css('a').attrib['href'],
            }
            
            yield scrapy.Request(url=item['url'], callback=self.parse_product, meta={'item': item})

    def parse_product(self, response):
        item = response.meta['item']

        # Scrape the product details based on <dt> and <dd>
        info_blocks = response.css('dl > div')
        for block in info_blocks:
            title = block.css('dt::text').get()
            value = block.css('dd[class="text-body-medium"]::text').get()
            if title and value:
                item[title] = value

        yield item

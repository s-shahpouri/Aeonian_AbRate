import scrapy

class ABspiderSpider(scrapy.Spider):
    name = 'scraper'
    allowed_domains = ['abcam.com']
    start_urls = ['https://www.abcam.com/en-nl/products/primary-antibodies']
    main = 'https://www.abcam.com'
    def parse(self, response):
        # <div class="pb-4 mb-4 border-b border-gray"><p class="font-bold text-gray-400 text-body-small">ab1791</p><p class="font-bold"><a href="/en-nl/products/primary-antibodies/anti-histone-h3-antibody-nuclear-marker-and-chip-grade-ab1791">Anti-Histone H3 antibody - Nuclear Marker and ChIP Grade</a></p><div class="flex pt-2 gap-2 flex-wrap"><div class="appearance-none px-2 py-1 rounded-4px bg-blue-5 text-xs font-semibold text-blue-default tracking-wider" data-testid="tag">Advanced Validation</div></div></div>
        products = response.css('div.pb-4')

        for product in products:
            yield{
                'name' : product.css('a::text').get(),
                'id' : product.css('p.font-bold::text').get(),
                'url' : product.css('a').attrib['href'],
            }

        next_page = response.css('a[aria-label="Next page"]::attr(href)').get()
        if next_page is not None:
            next_page_url = self.main + next_page
            print(next_page_url)
            yield response.follow(next_page_url, callback=self.parse)
        else:
            print("Url not found!")


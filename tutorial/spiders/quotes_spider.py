import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # 入口写法1
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    """
    start_requests方法的快捷方式
    无需实现从URL start_requests()生成scrapy.Request对象的方法，您只需定义start_urls带有URL列表的类属性即可。
    然后，默认实现的将使用此列表start_requests()为您的蜘蛛创建初始请求：
    """
    # 入口写法2
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

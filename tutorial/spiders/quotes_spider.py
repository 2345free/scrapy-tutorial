import scrapy

from tutorial.items import TutorialItem, ArticleItemLoader


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
        # 'http://quotes.toscrape.com/page/2/',
    ]

    # 覆盖全局设置
    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def parse(self, response):
        # 解析目录
        for quote in response.css('div.quote'):
            item_loader = ArticleItemLoader(item=TutorialItem(), selector=quote)
            item_loader.add_css('text', 'span.text::text')
            item_loader.add_css('author', 'small.author::text')
            item_loader.add_css('tags', 'div.tags a.tag::text')
            item_loader.add_value('url', response.url)
            item = item_loader.load_item()
            yield item

        # 获取下一页
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # 使用该urljoin()方法构建完整的绝对URL （因为链接可以是相对的）
            # next_page = response.urljoin(next_page)
            # yield Request(next_page, callback=self.parse)
            # 创建请求的捷径,直接支持相对URL-无需调用urljoin
            yield response.follow(next_page, callback=self.parse)

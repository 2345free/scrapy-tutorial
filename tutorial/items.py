# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst, MapCompose
from w3lib.html import remove_tags


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def remove_symbol(value):
    return value.replace('“', '').replace('”', '')


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    text = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_symbol)
    )
    author = scrapy.Field()
    tags = scrapy.Field(
        output_processor=Join(",")
    )
    url = scrapy.Field()
    screenshot_filename = scrapy.Field()

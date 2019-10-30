# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import json
import logging
from urllib.parse import quote

import mysql.connector
import pymongo
import scrapy


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.json', 'w')

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        logging.log(logging.INFO, 'item:%s', item)
        return item


class MongoPipeline(object):
    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


class ScreenshotPipeline(object):
    """Pipeline that uses Splash to render screenshot of
    every Scrapy item."""

    SPLASH_URL = "http://localhost:8050/render.png?url={}&render_all=1&wait=0.5"

    def process_item(self, item, spider):
        encoded_item_url = quote(item["url"])
        screenshot_url = self.SPLASH_URL.format(encoded_item_url)
        request = scrapy.Request(screenshot_url)
        dfd = spider.crawler.engine.download(request, spider)
        dfd.addBoth(self.return_item, item)
        return dfd

    def return_item(self, response, item):
        if response.status != 200:
            # Error happened, return item.
            return item

        # Save screenshot to file, filename will be hash of url.
        url = item["url"]
        url_hash = hashlib.md5(url.encode("utf8")).hexdigest()
        filename = "{}.png".format(url_hash)
        with open(filename, "wb") as f:
            f.write(response.body)

        # Store filename in item.
        item["screenshot_filename"] = filename
        return item


class MySQLPipeline(object):

    def __init__(self, config):
        # self.db = MySQLdb.connect(**config)
        self.cnx = mysql.connector.connect(**config)

    @classmethod
    def from_crawler(cls, crawler):
        config = {
            "host": crawler.settings.get('MYSQL_HOST'),
            "port": crawler.settings.get('MYSQL_PORT'),
            "db": crawler.settings.get('MYSQL_DB'),
            "user": crawler.settings.get('MYSQL_USER'),
            "passwd": crawler.settings.get('MYSQL_PASSWD'),
            "use_unicode": True,
            "charset": 'utf8',
        }
        return cls(config)

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        # self.db.close()
        self.cnx.close()

    def process_item(self, item, spider):
        logging.log(logging.INFO, 'item:%s', item)
        return item

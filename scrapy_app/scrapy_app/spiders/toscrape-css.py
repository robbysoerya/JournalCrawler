# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
import json
import re
import requests
from bs4 import BeautifulSoup
class MyItem(Item):
    url = Field()
    title = Field()

class ToScrapeCSSSpider(CrawlSpider):

    name = "toscrape-css"
    def __init__(self, *args, **kwargs):
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        ToScrapeCSSSpider.rules = [
            Rule(LinkExtractor(unique=True),
                 callback='parse_item', follow=True),
        ]
        super(ToScrapeCSSSpider, self).__init__(*args, **kwargs)

    # name = "toscrape-css"
    # allowed_domains = ['journal.uny.ac.id']
    # start_urls = [
    #     'https://journal.uny.ac.id/index.php/jpvo/about/siteMap',
    # ]
    # rules = (Rule(LinkExtractor(), callback='parse_url', follow=True),)


    def parse_item(self, response):
          
            # for link in LinkExtractor(allow=(), deny=self.allowed_domains).extract_links(response):
        item = MyItem()
        p = r"^\S*view\/\d*$"

        item['url'] = response.url
        item['title'] = response.css('title::text').getall()
        
        if(re.match(p,item['url'])):
            yield item

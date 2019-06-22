# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
import re
class MyItem(Item):
    url = Field()
    title = Field()
    reference = Field()

class ToScrapeCSSSpider(CrawlSpider):

    name = "toscrape-css"
    def __init__(self, *args, **kwargs):
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.limit = kwargs.get('limit')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.count = 0
        ToScrapeCSSSpider.rules = [
            Rule(LinkExtractor(unique=True),
                 callback='parse_item', follow=True),
        ]
        super(ToScrapeCSSSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
          
        item = MyItem()
        p = r"^\S*view\/\d*$"

        item['url'] = response.url
        item['title'] = response.css('title::text').getall()

        if(re.match(p,item['url'])):

            #Match reference with regex
            pattern = "^(\s*References\s*$)|(^\s*Referensi\s*$)"
            result = response.xpath('//*[text()[re:test(., "{}")]]/parent::*//text()'.format(pattern)).extract()
            
            #Remove control character like \n,\t, etc.
            t = dict.fromkeys(range(32))
            references = [x.translate(t) for x in result if x.translate(t) 
            and x.translate(t) != "References" and x.translate(t) != "Referensi"]
            
            item['reference'] = references
            
            if (self.count < int(self.limit)):
            #if(references):
                self.count += 1
                yield item
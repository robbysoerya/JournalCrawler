# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from scrapy.exceptions import CloseSpider
import re,os,requests
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
        self.task_id = kwargs.get('task_id')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.count = 0
        ToScrapeCSSSpider.rules = [
            Rule(LinkExtractor(unique=True),
                 callback='parse_item', follow=True),
        ]
        super(ToScrapeCSSSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):

        if (self.count < int(self.limit)):          
            item = MyItem()
            p = r"^\S*article\/view\/\d*$"

            item['url'] = response.url
            item['title'] = response.css('title::text').getall()

            dc = "//meta[@name='DC.{}']/@content"
            citation = "//meta[@name='citation_{}']/@content"

            author = response.xpath(dc.format('Creator.PersonalName')).extract()
            abstract = response.xpath(dc.format('Description')).extract()
            doi = response.xpath(dc.format('Identifier.DOI')).extract()
            issn = response.xpath(dc.format('Source.ISSN')).extract()
            issue = response.xpath(dc.format('Source.Issue')).extract()
            volume = response.xpath(dc.format('Source.Volume')).extract()
            title = response.xpath(dc.format('title')).extract()
            uri = response.xpath(dc.format('Identifier.URI')).extract()
            journal_title = response.xpath(citation.format('journal_title')).extract()
            author_institution = response.xpath(citation.format('author_institution')).extract()
            date = response.xpath(citation.format('date')).extract()
            keyword = response.xpath(citation.format('keywords')).extract()
            pdf = response.xpath(citation.format('pdf_url'))
            lan = response.xpath(citation.format('language')).extract() 

            if(re.match(p,item['url'])):

                #Match reference with regex
                pattern = "^(\s*References\s*$)|(^\s*Referensi\s*$)"
                result = response.xpath('//*[text()[re:test(., "{}")]]/parent::*//text()'.format(pattern)).extract()
                
                #Remove control character like \n,\t, etc.
                t = dict.fromkeys(range(32))
                references = [x.translate(t) for x in result if x.translate(t) 
                and x.translate(t) != "References" and x.translate(t) != "Referensi"]
                
                item['reference'] = references

                self.count += 1
                yield item        
        else:
            raise CloseSpider('limit reached')

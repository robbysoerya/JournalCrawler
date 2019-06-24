# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from scrapy.exceptions import CloseSpider
from scrapy.log import ERROR
import re,os,requests

class MyItem(Item):
    url = Field()
    title = Field()

class JournalItem(Item):
    title = Field()
    publisher = Field()
    volume = Field()
    issue = Field()
    issn = Field()

class ArticleItem(Item):
    title = Field()
    abstract = Field()
    doi = Field()
    publication_date = Field()
    keyword = Field()
    uri = Field()
    pdf_uri = Field()
    issn = Field()

class ReferencesItem(Item):
    title = Field()

class AuthorItem(Item):
    name = Field()
    affiliate = Field()

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

        if (self.count < int(self.limit)):          
            item = MyItem()
            item['url'] = response.url
            p = r"^\S*article\/view\/\d*$"

            if(re.match(p,item['url'])):

                journal = JournalItem()
                article = ArticleItem()
                references = ReferencesItem()
                author = AuthorItem()

                item['title'] = response.css('title::text').getall()

                dc = "//meta[@name='DC.{}']/@content"
                citation = "//meta[@name='citation_{}']/@content"

                author_name = response.xpath(dc.format('Creator.PersonalName')).extract()
                abstract = response.xpath(dc.format('Description')).extract_first()
                doi = response.xpath(dc.format('Identifier.DOI')).extract_first()
                issn = response.xpath(dc.format('Source.ISSN')).extract_first()
                issue = response.xpath(dc.format('Source.Issue')).extract_first()
                volume = response.xpath(dc.format('Source.Volume')).extract_first()
                title = response.xpath(dc.format('Title')).extract_first()
                uri = response.xpath(dc.format('Identifier.URI')).extract_first()
                journal_title = response.xpath(citation.format('journal_title')).extract_first()
                author_institution = response.xpath(citation.format('author_institution')).extract()
                date = response.xpath(citation.format('date')).extract_first()
                keyword = response.xpath(citation.format('keywords')).extract_first()
                pdf_uri = response.xpath(citation.format('pdf_url')).extract_first()
                lan = response.xpath(citation.format('language')).extract_first()

                article['title'] = title
                article['abstract'] = abstract
                article['doi'] = doi
                article['uri'] = uri
                article['pdf_uri'] = pdf_uri
                article['publication_date'] = date
                article['keyword'] = keyword
                article['issn'] = issn

                journal['title'] = journal_title
                journal['issn'] = issn
                journal['issue'] = issue
                journal['volume'] = volume
 
                author['name'] = author_name
                author['affiliate'] = author_institution

                #Match reference with regex
                pattern = "^(\s*References\s*$)|(^\s*Referensi\s*$)"
                result = response.xpath('//*[text()[re:test(., "{}")]]/parent::*//text()'.format(pattern)).extract()
                
                #Remove control character like \n,\t, etc.
                t = dict.fromkeys(range(32))
                ref = [x.translate(t) for x in result if x.translate(t) 
                and x.translate(t) != "References" and x.translate(t) != "Referensi"]
                
                references['title'] = ref
                self.count += 1
                yield {'journal' : journal, 'item' : item, 'article' : article, 
                'author' : author, 'references' : references}     
        else:
            raise CloseSpider('limit reached')
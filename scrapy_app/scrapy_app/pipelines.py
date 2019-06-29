from main.models import ScrapyItem,Journal,Article,Author,References
from django.core.exceptions import ObjectDoesNotExist
import json
class ReferencesAppPipeline(object):
    def __init__(self, publisher, *args, **kwargs):
        self.publisher = publisher

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # this will be passed from django view
            publisher=crawler.settings.get('publisher'),
        )

    def close_spider(self, spider):
        pass

    def process_item(self, references, spider):
        
        titles = references['references']['title']
        
        for title in titles:
            self.references = References()
            c_article_id = Article.objects.latest('c_article_id')
            self.references.c_article_id = c_article_id
            self.references.title = title
            self.references.save()

        return references

class AuthorAppPipeline(object):
    def __init__(self, publisher, *args, **kwargs):
        self.publisher = publisher

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # this will be passed from django view
            publisher=crawler.settings.get('publisher'),
        )

    def close_spider(self, spider):
        pass

    def process_item(self, author, spider):

        names = author['author']['name']
        affiliates = author['author']['affiliate']

        #Split 
        for i in range(len(names)):
            self.author = Author()
            c_article_id = Article.objects.latest('c_article_id')
            self.author.c_article_id = c_article_id
            self.author.name = names[i]
            self.author.affiliate = ""
            try:
                self.author.affiliate = affiliates[i]    
            except:
                self.author.save()
            
            self.author.save()    

        return author

class ArticleAppPipeline(object):
    def __init__(self, publisher, *args, **kwargs):
        self.publisher = publisher
    @classmethod

    def from_crawler(cls, crawler):
        return cls(
            # this will be passed from django view
            publisher=crawler.settings.get('publisher'),
        )

    def close_spider(self, spider):
        pass

    def process_item(self, article, spider):

        self.article = Article()

        #Get c_journal_id from exist issn
        journal = Journal.objects.get(issn=article['article']['issn'])

        self.article.c_journal_id = journal
        self.article.title = article['article']['title']
        self.article.abstract = article['article']['abstract']
        self.article.doi = article['article']['doi']
        self.article.keyword = article['article']['keyword']
        self.article.publication_date = article['article']['publication_date']
        self.article.uri = article['article']['uri']
        self.article.pdf_uri = article['article']['pdf_uri']
        self.article.save()

        return article

class JournalAppPipeline(object):
    def __init__(self, publisher, *args, **kwargs):
        self.publisher = publisher

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # this will be passed from django view
            publisher=crawler.settings.get('publisher'),
        )

    def close_spider(self, spider):
        pass

    def process_item(self, journal, spider):

        self.journals = Journal()
        self.journals.title = journal['journal']['title']
        self.journals.volume = journal['journal']['volume']
        self.journals.issue = journal['journal']['issue']
        self.journals.issn = journal['journal']['issn']
        self.journals.publisher = self.publisher
        
        #Check exist journal, if exist, skip
        try:
            if Journal.objects.get(issn=journal['journal']['issn']):
                pass   
        except ObjectDoesNotExist:
            self.journals.save()
        return journal

class ScrapyAppPipeline(object):
    def __init__(self, unique_id, stats, publisher, *args, **kwargs):
        self.unique_id = unique_id
        self.stats = stats
        self.publisher = publisher
        self.items = []
        self.item_all = ScrapyItem()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # this will be passed from django view
            unique_id=crawler.settings.get('unique_id'), 
            publisher=crawler.settings.get('publisher'),
            stats=crawler.stats
        )

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.items.append({'url':item['item']['url'],'title':item['item']['title']})
        self.item_all.unique_id = self.unique_id
        self.item_all.data = json.dumps(self.items)
        if self.stats.get_value('item_scraped_count'):
            self.item_all.item_scraped = self.stats.get_value('item_scraped_count')
        else:
            pass
        self.item_all.save()

        return item

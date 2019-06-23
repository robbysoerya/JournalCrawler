from main.models import ScrapyItem
import json

class ScrapyAppPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id
        self.items = []
        self.itema = ScrapyItem()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
        )

    def close_spider(self, spider):
        # And here we are saving our crawled data with django models.
        
        pass

    def process_item(self, item, spider):
        self.items.append({'url':item['url'],'title':item['title'],'reference':item['reference']})
        self.itema.unique_id = self.unique_id
        self.itema.data = json.dumps(self.items)
        self.itema.save()
        return item

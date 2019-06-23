import json
from django.db import models
from django.utils import timezone


class Journal(models.Model):
    c_journal_id = models.AutoField(primary_key=True)
    title = models.TextField()
    publisher = models.TextField()
    volume = models.TextField(null=True)
    issue = models.TextField(null=True)
    issn = models.TextField()

    def __str__(self):
        return self.title    

class Article(models.Model):
    c_article_id = models.AutoField(primary_key=True)
    title = models.TextField()
    abstract = models.TextField(null=True)
    doi = models.TextField(unique=True)
    publication_date = models.TextField(null=True)
    keyword = models.TextField(null=True)
    uri = models.TextField(null=True)
    pdf_uri = models.TextField(null=True)

    c_journal_id = models.ForeignKey('Journal',on_delete=models.PROTECT)

    def __str__(self):
        return self.title

class References(models.Model):
    c_references_id = models.AutoField(primary_key=True)
    title = models.TextField(null=True)
    c_article_id = models.ForeignKey('Article', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.c_article_id)

class Author(models.Model):
    c_author_id = models.AutoField(primary_key=True)
    name = models.TextField()
    affiliate = models.TextField(null=True)
    c_article_id = models.ForeignKey('Article', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.c_article_id)

class ScrapyItem(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    data = models.TextField()  # this stands for our crawled data
    date = models.DateTimeField(default=timezone.now)

    # This is for basic and custom serialisation to return it to client as a JSON.
    @property
    def to_dict(self):
        data = {
            'data': json.loads(self.data),
            'date': self.date
        }
        return data

    def __str__(self):
        return self.unique_id

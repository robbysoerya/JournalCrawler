# Generated by Django 2.2.2 on 2019-06-25 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_scrapyitem_item_scraped'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='language',
            field=models.TextField(default=' ', null=True),
        ),
    ]

# Generated by Django 2.2.2 on 2019-07-04 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_article_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='references',
            name='classification',
            field=models.TextField(null=True),
        ),
    ]

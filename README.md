# Journal Crawler

* Basic structure of a Django project.
* Basic structure for scrapy.
* Configuration of scrapy in order to access Django models objects.
* Basic scrapy pipeline to save crawled objets to Django models.
* Basic spider definition
* Simple front end with React

## Setup
1 - Install requirements
````
$ pip install -r requirements.txt
````
2 - Configure the database
````
$ python manage.py migrate
````
## Start the project
In order to start this project you will need to have running Django and Scrapyd at the same time.

In order to run Django
````
$ python manage.py runserver
````
In order to run Scrapyd
````
$ cd scrapy_app
$ scrapyd
````

At this point you will be able to send job request to Scrapyd. This project is setup with a demo spider from the oficial tutorial of scrapy. To run it you must send a http request to Scrapyd with the job info
````
curl http://localhost:6800/schedule.json -d project=default -d spider=toscrape-css
````

The crawled data will be automatically be saved in the Django models

This repo is inspired by an article from Ali Oğuzhan Yıldız, https://medium.com/@ali_oguzhan/how-to-use-scrapy-with-django-application-c16fabd0e62e

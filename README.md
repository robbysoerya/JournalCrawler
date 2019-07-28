# Journal Crawler

* Used Python3.6
* Database with PostgreSQL
* Structure of a Django project.
* Structure for scrapy.
* Configuration of scrapy in order to access Django models objects.
* Scrapy pipeline to save crawled objets to Django models.
* Machine Learning with Random Forest
* React for Front End

## Setup
1 - Install requirements
````
$ pip3 install -r requirements.txt
````
2 - Configure the database
````
$ vi iCrawler/settings.py
````
3 - Apply changes
```
$ python manage.py migrate
```
4 - Change location of model Random Forest [Line 129 & 136]
```
$ vi scrapy_app/scrapy_app/spiders/toscrape-css.py
```

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
http://localhost:8000/home
````

The crawled data will be automatically be saved in the Django models.
To view database of crawler with Django Admin
```
http://localhost:8000/admin
```

To check jobs log
```
http://localhost:6800
```

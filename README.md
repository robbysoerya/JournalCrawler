# Journal Crawler

* Structure of a Django project.
* Structure for scrapy.
* Configuration of scrapy in order to access Django models objects.
* Scrapy pipeline to save crawled objets to Django models.
* Front end with React

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
open in browser http://localhost:8000/home
````

The crawled data will be automatically be saved in the Django models.
To view database of crawler with Django Admin
```
open in browser http://localhost:8000/admin
```
from django.conf import settings
from django.conf.urls import url, static,include
from django.urls import path
from django.views.generic import TemplateView
from main import views
from django.contrib import admin

urlpatterns = [
    path(r'home/', include('frontend.urls')),
    url(r'^api/crawl/', views.crawl, name='crawl'),
    url(r'^admin/', admin.site.urls),
]

# This is required for static files while in development mode. (DEBUG=TRUE)
# No, not relevant to scrapy or crawling :)
if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static.static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

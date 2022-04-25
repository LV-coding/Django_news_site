from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import News

class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ['index', 'login', 'register', 'about', 'savednews', 'currency', 'mylinks', 'robots']

    def location(self, item):
        return reverse(item)

"""
class DateSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https' 

    def items(self):
        all_news = News.objects.all()

"""
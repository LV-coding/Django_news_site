from ast import Delete
from audioop import maxpp
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils import timezone

class User(AbstractUser):
    us_id = models.AutoField(primary_key=True)


class News_site(models.Model):
    news_site_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    url = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    news_site = models.ForeignKey(News_site, on_delete=models.CASCADE, related_name="news_site")
    news_title = models.CharField(max_length=128)
    news_url = models.CharField(max_length=256)
    add_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.news_site}: {self.news_title}'   

    def show_date(self):
        return self.add_date.strftime('%Y-%m-%d')

    def check_old_date(self):                               # use for delete old news
        storage_days_limit = timedelta(days=45)
        today = timezone.now()
        if (today - self.add_date) > storage_days_limit:
            return True
        else:
            return False


class SaveNews(models.Model):
    save_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    news_save = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news_save")
    save_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.news_save}'


# Own user links
class Link(models.Model):
    link_id = models.AutoField(primary_key=True)
    link_url = models.CharField(max_length=256)
    link_title = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link_add_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user}__{self.link_title}'




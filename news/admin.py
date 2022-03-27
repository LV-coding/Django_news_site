from django.contrib import admin
from .models import User, News_site, News, SaveNews, Link

class NewsAdmin(admin.ModelAdmin):
    list_display = ("news_site", "add_date", "news_title")

admin.site.register(User)
admin.site.register(News_site)
admin.site.register(News, NewsAdmin)
admin.site.register(SaveNews)
admin.site.register(Link)

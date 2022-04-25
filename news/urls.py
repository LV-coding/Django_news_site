from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticSitemap

sitemaps = {
    'static':StaticSitemap
}

urlpatterns = [
    path('', views.index, name="index" ),
    path('login', views.login_view, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('about', views.about, name="about"),
    path('update', views.update, name="update"),
    path('savednews', views.saved_news, name="savednews"),
    path('save/<int:news_id>', views.save_news, name="save"),
    path('unsave/<int:news_id>', views.unsave_news, name="unsave"),
    path('search/', views.search, name="search"),
    path('currency', views.currency, name="currency"),
    path('mylinks', views.saved_links, name="mylinks"),
    path('mylinks/<int:link_id>/delete_link', views.delete_link, name="delete_link"),
    path('mylinks/<int:link_id>/edit_link', views.edit_link, name="edit_link"),
    path('date/<date>', views.date_view, name="date"),
    path('robots.txt', views.robots, name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]





 

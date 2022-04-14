from django.urls import path
from . import views

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
    path('delete_link/<int:link_id>', views.delete_link, name="delete_link"),
    path('edit_link/<int:link_id>', views.edit_link, name="edit_link"),
    path('date/<date>', views.date_view, name="date"),
    path('sitemap.xml', views.site_map, name='sitemap'),
    path('robots.txt', views.robots, name='robots')
]





 

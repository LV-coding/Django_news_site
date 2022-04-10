from sys import exec_prefix
from django.shortcuts import render
from .models import User, News, SaveNews, Link
from functools import lru_cache
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from time import sleep
import datetime
from math import ceil
from threading import Thread
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.contrib.auth.decorators import login_required

@lru_cache(maxsize=None)
def index(request):
    all_news = News.objects.all().order_by("-add_date")
    link_per_page = 40                                      # 25 news in each page

    # If the database is empty. It's need only at start
    try:
        paginator = Paginator(all_news, link_per_page) 
    except:
        paginator = 0
        
    try:
        # For create url and choose default value paginations
        num = request.GET.get('index', '1')
        page = paginator.page(num) 
    except PageNotAnInteger:  
        # If numbers of page is not integer values render 1 page
        page = paginator.page(1)  
    except EmptyPage:  
        # If in url entered more values than there are pages, then select the latter
        page = paginator.page(paginator.num_pages)
    except:
        page = []

    try:
        # for render number max page
        counter_page = ceil(len(all_news)/link_per_page)
    except:
        counter_page = 0
    return render(request, "news/index.html", {
        "paginator": paginator,
        "page": page,
        "counter_page": counter_page
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        email = request.POST["email"]

        # Checking password
        if password != confirm_password:
            return render(request, "news/register.html", {
                "message":"Паролі мають співпадати."
            })

        # Checking the uniqueness of the user
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            return render(request, "news/register.html", {
                "message":"Такий користувач вже існує."
            })

        # if future user does not enter the data in the form
        except ValueError:
            return render(request, "news/register.html", {
                "message":"Помилка значень."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "news/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password )
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "news/login.html", {
                "message":"Невірний логін або пароль."
            })
    else:
        return render(request, "news/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def about(request):
    return render(request, "news/about.html")


def saved_news(request):
    try:
        all_news = SaveNews.objects.filter(user=request.user).order_by('-save_date')
    except:
        all_news = []
    
    # The message shows only unlogged
    return render(request, "news/savednews.html", {
    "message": "Для використання цього функціоналу Ви повинні бути залоговані.",
    "all_news": all_news
    })


@login_required
def save_news(request, news_id):
    news = News.objects.get(news_id=news_id)
    list_news = SaveNews.objects.filter(user=request.user, news_save=news)

    # Check for saved news. If there is, do nothing
    flag = False
    for i in list_news:
        if i.news_save == news:
            flag = True
    if not flag:
        news = SaveNews(user=request.user, news_save=news)
        news.save()
    return HttpResponseRedirect(reverse("index"))


@login_required
def unsave_news(request, news_id):
    this_news = News.objects.get(news_id=news_id)
    news = SaveNews.objects.get(user=request.user, news_save=this_news)
    news.delete()
    return HttpResponseRedirect(reverse("savednews"))


@login_required
def update(request):
    # This is an admin tool for unscheduled parsing.
    if request.user.is_superuser:
        util.get_minfin()
        util.get_e_pravda()  
        util.get_e_sogodni()
        util.get_unn()
        util.get_unian()
        util.get_shlyahta()
        util.get_ukrinform()
        return HttpResponseRedirect(reverse("index"))  
    else:
        return HttpResponseRedirect(reverse("index"))     


def search(request):           
    if request.method == "GET":
        search_text = request.GET.get('q')
        search_words = search_text.split(', ')
        len_search_words = len(search_words)
        result = []
        all_news = News.objects.all()

        # Checking each news item for each search word
        for news in all_news:
            res = 0
            for word in search_words:
                if word.lower() in news.news_title.lower():
                    res +=1
            if res == len_search_words:
                result.insert(0, news)

        return render(request, "news/search.html", {
            "result": result,
            "counter": len(result),
            "search_text": search_text                     
        })

        

def currency(request): # in plans...
    return render(request, "news/currency.html")


# Functionality for users to save their links
@login_required
def saved_links(request):
    if request.user.is_superuser:
        try:
            all_links = Link.objects.all().filter(user=request.user).order_by('-link_add_date')
        except:
            all_links = []
        if request.method == 'POST':
            link_title = request.POST["link_title"]
            link_url = request.POST["link_url"]
            link = Link(link_title=link_title, link_url=link_url, user = request.user)
            link.save()
            return HttpResponseRedirect(reverse("mylinks"))   
        return render(request, "news/mylinks.html", {
            "all_links": all_links
        })
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def delete_link(request, link_id):
    link = Link.objects.get(link_id=link_id)
    if request.user == link.user:
        link.delete()
        return HttpResponseRedirect(reverse("mylinks"))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def edit_link(request, link_id):
    link = Link.objects.get(link_id=link_id)
    if request.user == link.user:
        if request.method == "POST":
            link.link_title = request.POST["link_title"]
            link.link_url = request.POST["link_url"]
            link.user = request.user
            link.save()
            return HttpResponseRedirect(reverse("mylinks"))
        else:
            return render(request, "news/edit_link.html", {
                "link": link
            })
    else:
        return HttpResponseRedirect(reverse("index"))


def unknown_page(request, some_text):
    return render(request,  "news/unknown.html", {
        "some_text": some_text
    })

@lru_cache(maxsize=None)
def date_view(request, date):
    list_news = News.objects.all().order_by("-add_date")
    all_news = (news for news in list_news if news.show_date() == date)
    return render(request, "news/date.html", {
        "all_news": all_news,
        "date": datetime.date(int(date[:4]), int(date[-5:-3]), int(date[-2:]))
    })


# This function runs in another thread
def create_db_and_start_parser():
    util.create_news_site()
    # k = 0

    while True:
        time_sleep = 150

        util.get_minfin()
        sleep(time_sleep)

        util.get_unian()
        sleep(time_sleep)

        util.get_e_pravda()
        sleep(time_sleep)

        util.get_e_sogodni()
        sleep(time_sleep)

        util.get_unn()
        sleep(time_sleep)

        util.get_shlyahta()
        sleep(time_sleep)
        
        util.get_ukrinform()
        sleep(time_sleep)
        """
        k +=1

        if k >= 1:
            all_news = News.objects.all()
            len_all_news = len(all_news)
            delete_limit = 50

            if len_all_news > delete_limit:
                news_for_delete = all_news[:(len_all_news-delete_limit)]
                for i in news_for_delete:
                    i.delete()
                    i.save()

            k = 0
        """


# Launch another thread
x = Thread(target=create_db_and_start_parser, args=(), daemon=True)
x.start()
 



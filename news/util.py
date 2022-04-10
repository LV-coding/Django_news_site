import requests
from bs4 import BeautifulSoup
from .models import News, News_site


def create_news_site():

    url = "https://minfin.com.ua/ua/news/"
    title = "МінФін"
    if not News_site.objects.all().filter(url=url):
        site = News_site(title=title, url=url)
        site.save()

    url = "https://www.epravda.com.ua/news/"
    title = "Економічна правда"
    if not News_site.objects.all().filter(url=url):
        site = News_site(title=title, url=url)
        site.save()

    url = "https://economics.segodnya.ua/ua"
    title = "Сьогодні"
    if not News_site.objects.all().filter(url=url):
        site = News_site(title=title, url=url)
        site.save()

    url = "https://www.unn.com.ua/uk/news/economics"
    title = "УНН"
    if not News_site.objects.all().filter(url=url):
        site = News_site(title=title, url=url)
        site.save()

    url = "https://www.unian.ua/detail/all_news/economics"
    title = "УНІАН"
    if not News_site.objects.all().filter(url=url):
        site = News_site(title=title, url=url)
        site.save()

    url = "https://shlyahta.com.ua"
    title = "Шляхта не працює"
    if not News_site.objects.all().filter(url=url):
        site = News_site(title=title, url=url)
        site.save()

    url = "https://www.ukrinform.ua/rubric-economy/block-lastnews"
    title = "Укрінформ"
    if not News_site.objects.all().filter(url=url):
        site = News_site(title=title, url=url)
        site.save()
    


# Here and below are parsers of various sites
def get_minfin():

    url = "https://minfin.com.ua/ua/news/"
    site_name = News_site.objects.get(url=url)

    response = requests.get(url)                                    # connect with site
    if response.status_code == 200:                                 # if connect succesful
        soup = BeautifulSoup(response.content, 'html.parser')       # parsing
        for i in soup.find_all("li", class_="item"):                # search news, in other parser may differ
            try:                                                    # some sites have empty news feeds
                i = i.find('a')                                     # find news url
                href =f'https://minfin.com.ua{i["href"]}'           # change url for writing 
                title = i.text                                      # get news title
                if not News.objects.all().filter(news_url=href):    # if news url not in DB write it
                    news = News(news_site=site_name, news_url=href, news_title=title)
                    news.save()
                else:   
                    break                                           # if url in basis further check is not required                                   
            except:
                pass


def get_e_pravda():

    url = "https://www.epravda.com.ua/news/"
    site_name = News_site.objects.get(url=url)

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for i in soup.find_all("div", class_="article__title"):
            try:
                i = i.find('a')
                href =f'https://www.epravda.com.ua{i["href"]}'
                title = i.text
                if not News.objects.all().filter(news_url=href):
                    news = News(news_site=site_name, news_url=href, news_title=title)
                    news.save()
                else:
                    break
            except:
                pass


def get_e_sogodni():

    url = "https://economics.segodnya.ua/ua"
    site_name = News_site.objects.get(url=url)

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for i in soup.find_all("h4", class_="b-article__title"):
            try:
                i = i.find('a')
                href =i["href"]
                title = i.text
                if not News.objects.all().filter(news_url=href):
                    news = News(news_site=site_name, news_url=href, news_title=title)
                    news.save()
                else:
                    break
            except:
                pass     
        

def get_unn():  #?

    url = "https://www.unn.com.ua/uk/news/economics"
    site_name = News_site.objects.get(url=url)

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for i in soup.find_all("p", class_="title"):
            try:
                i = i.find('a')
                href =f'https://www.unn.com.ua{i["href"]}'
                title = i.text
                if not News.objects.all().filter(news_url=href):
                    news = News(news_site=site_name, news_url=href, news_title=title)
                    news.save()
                else:
                    break
            except:
                pass


def get_unian():    #403

    url = "https://www.unian.ua/detail/all_news/economics"
    site_name = News_site.objects.get(url=url)

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for i in soup.find_all("div", class_="list-thumbs__info"):
            try:
                i = i.find('a')
                href =i["href"]
                title = i.text
                if not News.objects.all().filter(news_url=href):
                    news = News(news_site=site_name, news_url=href, news_title=title)
                    news.save()
                else:
                    break
            except:
                pass


def get_shlyahta():

    url = "https://shlyahta.com.ua"
    site_name = News_site.objects.get(url=url)

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for i in soup.find_all("h2", class_="entry-title"):
            try:
                i = i.find('a')
                href =i["href"]
                title = i.text
                if not News.objects.all().filter(news_url=href):
                    news = News(news_site=site_name, news_url=href, news_title=title)
                    news.save()
                else:
                    break
            except:
                pass


def get_ukrinform():

    url = "https://www.ukrinform.ua/rubric-economy/block-lastnews"
    site_name = News_site.objects.get(url=url)

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for i in soup.find("div", class_="othersBody"):
            try:
                i = i.find('a')
                href =f'https://www.ukrinform.ua{i["href"]}'
                title = i["title"][12:] 
                if not News.objects.all().filter(news_url=href) and not News.objects.all().filter(news_title=title, news_site=site_name):
                    news = News(news_site=site_name, news_url=href, news_title=title)
                    news.save()
                else:
                    break
            except:
                pass



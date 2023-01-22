import requests
from bs4 import BeautifulSoup
import json
import flask


app = flask.Flask(__name__)
headers = {"User-Agent":"Mozilla/5.0"}

@app.route('/fun_news')
def fetch_news_fun():
    newsdict = {}
    headers = {"User-Agent":"Mozilla/5.0"}

    with requests.Session() as session:
        session.headers = headers
        read = session.get("https://www.upi.com/Odd_News/")

        newsdict['url'] = "https://www.upi.com/Odd_News/"
        newsdict['status'] = "{}".format(read.status_code)

        soup = BeautifulSoup(read.content,'html.parser')

        i = 1
        for article in soup.find_all("a", "row")[:5]:
            newsdict["id {}".format(i)] = {
                'url':article.get('href'),
                'title':article.get('title'),
                'image':article.find('img').get('src'),
                'description': article.find('div',{'class':'content'}).text[16:]
            }

            i += 1

        newsdict = json.dumps(newsdict,indent=2)
        return newsdict

@app.route('/bollywood')
def fetch_news_entertain():
    newsdict = {}

    with requests.Session() as session:
        session.headers = headers
        read = session.get("https://www.bollywoodhungama.com/")

        newsdict['url'] = "https://www.bollywoodhungama.com/"
        newsdict['status'] = "{}".format(read.status_code)

        soup = BeautifulSoup(read.content,'html.parser')

        i = 1
        soup = soup.find("div", id = "trending-live")
        for article in soup.find("ul","large-6 medium-6 small-12 columns no-bullet"):

            newsdict["id {}".format(i)] = {

                'url':article.find('a').get('href'),
                'title':article.find('a').get('title'),
                'image':article.find('img').get('src'),
                'description':article.find('a').get('title')
            }

            i += 1

        newsdict = json.dumps(newsdict,indent=4)

        return newsdict


@app.route('/infotainment')
def fetch_news_positive():
    
    A = {}

    with requests.Session() as session:
        session.headers = headers

        read = session.get("https://www.positive.news/")


        soup = BeautifulSoup(read.content,'html.parser')

        i = 1
        for article in soup.select("div.column.card"):

            articlesession = session.get(article.find('a').get('href'))
            articlesoup = BeautifulSoup(articlesession.content,'html.parser')

            A[i] = {
                "url":article.find('a').get('href'),
                "image":articlesoup.find('img').get('src'),
                "title":articlesoup.find('h1').text,
                "description":articlesoup.select_one("div.intro__paragraph").text
            }

            i += 1
    newsdict = json.dumps(A,indent=2)

    return A
@app.route('/fraud_alert')
def fetch_news_fraud():
    newsdict = {}

    with requests.Session() as session:
        session.headers = headers
        read = session.get("https://www.ic3.gov/")

        soup = BeautifulSoup(read.content,'html.parser')

        i = 1
        for article in soup.find_all("div","card border-0")[:4]:
            
            articlesession = session.get(article.find('a').get('href'))
            articlesoup = BeautifulSoup(articlesession.content,'html.parser')

            desc = articlesoup.find_all('p')[2]

            newsdict["id {}".format(i)] = {
                'url': article.find('a').get('href'),
                'title' : article.find('a').get('title'),
                'image' : "https://en.wikipedia.org/wiki/Symbols_of_the_Federal_Bureau_of_Investigation#/media/File:Seal_of_the_Federal_Bureau_of_Investigation.svg",
                'description' : desc.text
            }

            i += 1

        newsdict = json.dumps(newsdict,indent=2)

        return newsdict


if(__name__ == "__main__"):
     app.run(debug=True)

     
                
                


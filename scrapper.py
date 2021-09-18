import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta
import ujson 

time = datetime.now()
date = datetime.strptime("2014-05","%Y-%m")
json = ujson.loads(open("articles.json").read())

i = 0

while date<time:
    if date.month == 7:
        date += relativedelta(months=+1)
    URL = f"https://www.1lo.pl/?arch={date.strftime('%Y-%m')}"

    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    newses = soup.find_all("div",class_="news e-")
    for news in newses:

        try:
            news_img = news.find_all("img")[0]['src']
        except:
            news_img = None
        news_title = news.find_all("div",class_="title")[0].text
        news_date = news.find_all("div",class_="date")[0].text
        news_content = news.find_all("div",class_="header")[0].text
        
        print(news_date)

        json[i] = {}
        json[i]['image'] = news_img
        json[i]['title'] = news_title
        json[i]['date'] = news_date
        json[i]['content'] = news_content
        i += 1

    date += relativedelta(months=+1)
    

f = open("articles.json","w",encoding="utf-8")
ujson.dump(json,f)

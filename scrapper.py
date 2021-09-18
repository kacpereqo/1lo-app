import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta
import ujson 

time = datetime.now()
date = datetime.strptime("2014-05","%Y-%m")

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
        # f=open("b.txt","w",encoding="utf-8")
        # f.write(news_content)

        headers = {'accept': 'application/json','Content-Type': 'application/json'}

        data = ujson.dumps({"title": news_title,"date": news_date,"img": news_img,"content": news_content})
        requests.put("http://127.0.0.1:8000/article",data=data,headers=headers)

    date += relativedelta(months=+1)
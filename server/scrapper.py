import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta
import ujson 
import sqlite3

time = datetime.now()
date = datetime.strptime("2014-05","%Y-%m")
conn = sqlite3.connect("db/articles.db",check_same_thread=False)

c = conn.cursor()
c.execute("""CREATE TABLE articles(
    id integer primary key autoincrement,
    title text,
    img text,
    date text,
    content text)""")

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
            news_img = "https://www.1lo.pl/files/news/logo_33.jpg"
        news_title = news.find_all("div",class_="title")[0].text
        news_date = news.find_all("div",class_="date")[0].text
        news_content = news.find_all("div",class_="header")[0].text

        with conn:
            c.execute("SELECT 1 FROM 'articles' WHERE title = (:title) AND date = (:date)",{"title":news_title,"date":news_date})   
            if not c.fetchone():
                headers = {'accept': 'application/json','Content-Type': 'application/json'}
                data = ujson.dumps({"title": news_title,"date": news_date,"img": news_img,"content": news_content})
                requests.put("http://127.0.0.1:8000/article",data=data,headers=headers)
                print(news_date)
            

    date += relativedelta(months=+1)
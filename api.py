from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

conn = sqlite3.connect("articles.db",check_same_thread=False)
c = conn.cursor()
app = FastAPI()

class Article(BaseModel):
    title: str
    date: str
    img: str
    content: str

def insert(article):
    with conn:
        c.execute("INSERT INTO articles VALUES (?,?,?,?,?)",(None,article.title, article.img, article.date, article.content))
        print("article has been inserted")

@app.on_event("shutdown")
def shutdown_event():
    conn.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/article/latest")
def latest_article():
    return "latest"

@app.get("/article/latest/{latest}")
def latest_articles(latest:int):
    return f"{latest} articles"


@app.put("/article")
def put_article(article: Article):
    insert(article)
    return "done"
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# uvicorn api:app --reload

conn = sqlite3.connect("db/articles.db",check_same_thread=False)
c = conn.cursor()
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Article(BaseModel):
    title: str
    date: str
    img: str
    content: str

def insert(article):
    with conn:
        c.execute("INSERT INTO articles VALUES (?,?,?,?,?)",(None,article.title, article.img, article.date, article.content))

def get(range_):
    with conn:
        c.execute("SELECT * FROM 'articles' ORDER BY id DESC LIMIT (:range)",{"range":range_})     
        return c.fetchall()

@app.on_event("shutdown")
def shutdown_event():
    conn.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/article/latest/{range_}")
def latest_articles(range_:int):
    values = get(range_)
    dct = {}
    for i,value in enumerate(values):
        dct[i] = {"id":value[0],"title":value[1],"date":value[2],"img":value[3],"content":value[4]}
    return dct


@app.put("/article")
def put_article(article: Article):
    insert(article)
    return "done"

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
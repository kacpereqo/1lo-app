import sqlite3

conn = sqlite3.connect("articles.db",check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE articles (
    id integer primary key autoincrement,
    title text,
    img text,
    date text,
    content text
)""")


conn.commit()        
conn.close()
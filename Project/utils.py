import sqlite3


DB_NAME = 'projects.db'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}


def connect_db():
    conn = sqlite3.connect(DB_NAME)
    return conn


def create_table(conn):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS projects
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    link TEXT NOT NULL,
                    description TEXT)''')
    conn.commit()


def insert_data(conn, data):
    cur = conn.cursor()
    cur.execute('''INSERT INTO projects(title, link, description)
                   VALUES (?, ?, ?)''', (data['title'], data['link'], data['description']))
    conn.commit()

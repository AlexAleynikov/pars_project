import requests
from bs4 import BeautifulSoup
import sqlite3

DB_NAME = 'projects.db'
HOST = 'https://www.freelancer.com.ua/'
URL = 'https://www.freelancer.com.ua/jobs'
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


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='JobSearchCard-item-inner')
    works = []

    for item in items:
        title_elem = item.find('a', class_='JobSearchCard-primary-heading-link')
        if title_elem:
            title = title_elem.get_text(strip=True)
            link = title_elem.get('href')
            description_elem = item.find('p', class_='JobSearchCard-primary-description')
            description = description_elem.get_text(strip=True) if description_elem else ''
            works.append({
                'title': title,
                'link': HOST + link,
                'description': description
            })
    return works


def parser():
    conn = connect_db()
    create_table(conn)
    html = get_html(URL)
    if html.status_code == 200:
        for page in range(1, 4):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'page': page})
            page_content = get_content(html.text)
            if not page_content:
                break
            for item in page_content:
                insert_data(conn, item)
    else:
        print('Error')


if __name__ == '__main__':
    parser()

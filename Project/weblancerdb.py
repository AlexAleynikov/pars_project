import requests
from bs4 import BeautifulSoup
from utils import HEADERS, connect_db, create_table, insert_data


HOST = 'https://www.weblancer.net/'
URL = 'https://www.weblancer.net/jobs/'


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='row click_container-link set_href')
    works = []

    for item in items:
        title_elem = item.find('a', class_='text-bold click_target show_visited')
        if title_elem:
            title = title_elem.get_text(strip=True)
            link = title_elem.get('href')
            description_elem = item.find('span', class_='snippet')
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

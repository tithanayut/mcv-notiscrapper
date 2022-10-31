import re
import requests
from bs4 import BeautifulSoup
from notification import Notification


class Scraper:
    def __init__(self):
        self.s = requests.Session()
        self.init()

    def init(self):
        r = self.s.get(
            'https://www.mycourseville.com/api/oauth/authorize?response_type=code&client_id=mycourseville.com&redirect_uri=https://www.mycourseville.com')
        soup = BeautifulSoup(r.text, 'html.parser')
        self.form_token = soup.find('input', {'name': '_token'}).get('value')

    def login(self, username, password):
        r = self.s.post('https://www.mycourseville.com/api/login', data={
            '_token': self.form_token,
            'loginfield': 'name',
            'name': username,
            'password': password
        })
        if r.status_code != 200:
            raise Exception("Login failed")

    def scrape(self):
        r = self.s.get(
            'https://www.mycourseville.com/?q=courseville/course/notification')
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all('a', {'class': 'courseville-feed-item'})

        notifications = []
        for item in items:
            notifications.append(Notification(
                course=item.find(
                    'div', {'class': 'courseville-feed-item-course'}).text.strip(),
                type=item.find(
                    'div', {'class': 'courseville-feed-item-type'}).text.strip(),
                title=item.find(
                    'div', {'class': 'courseville-feed-item-title'}).text.strip(),
                created=re.search(r"Created on (.+)      -- (?:.+)", item.find(
                    'div', {'class': 'courseville-feed-item-created'}).text).group(1),
                icon_img=item.find(
                    'img', {'class': 'courseville-feed-item-icon-img'}).get('src'),
                link=item.get("href")
            ))
        return notifications

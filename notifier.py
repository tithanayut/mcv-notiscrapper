import requests


class Notifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, course, type, title, link):
        r = requests.post(self.webhook_url, json={
            "blocks": [
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": course
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*{type.capitalize()}*: <https://www.mycourseville.com{link}|{title}>"
                        }
                    ]
                },
                {
                    "type": "divider",
                },
            ]
        })
        if r.status_code != 200:
            raise Exception("Notification failed")

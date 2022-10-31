import os
from scraper import Scraper
from recorder import Recorder
from notifier import Notifier

MCV_USERNAME = os.environ.get("MCV_USERNAME")
MCV_PASSWORD = os.environ.get("MCV_PASSWORD")
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")


def main():
    scraper = Scraper()
    notifier = Notifier(SLACK_WEBHOOK_URL)
    recorder = Recorder("records.csv")

    scraper.login(MCV_USERNAME, MCV_PASSWORD)

    notifications = scraper.scrape()
    for notification in notifications:
        print(f"Processing ${notification.type} - ${notification.title}")
        if recorder.is_exist(notification.course,
                             notification.type,
                             notification.title,
                             notification.created):
            continue

        recorder.record(
            notification.course,
            notification.type,
            notification.title,
            notification.created
        )

        print(f"Sending ${notification.type} - ${notification.title} to Slack")
        notifier.send(
            notification.course,
            notification.type,
            notification.title,
            notification.link
        )

    recorder.done()


if __name__ == '__main__':
    main()

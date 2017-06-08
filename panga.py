from db import DB
from mail import Mail
import time
from datetime import datetime
import card

m = Mail()
db = DB()


def main():
    today = None
    while True:
        if today == None or today != datetime.today():
            remind()
            today = datetime.today()

        # sleep 5 mintues
        check_mail()
        time.sleep(60)


def check_mail():
    content = m.receive()
    db.insert([card.Card(c).to_hash() for c in content])


def remind():
    cards = [card.load(c) for c in db.read()]
    remind_body = []
    splitter = "\n\n---------------------------------\n\n"
    header = "This is what you need to review: \n\n #################### \n\n"
    for c in cards:
        if c.should_remind():
            remind_body.append(c.content)
            c.round += 1

    db.write([c.to_hash() for c in cards])
    if remind_body:
        m.send(m.config['notifier']['email'], '[Panga] Remind',
               header + splitter.join(remind_body))


if __name__ == '__main__':
    main()

from db import DB
from mail import Mail
import time
from datetime import datetime
import card
import pdb

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
        time.sleep(5*60)


def check_mail():
    content = m.receive()
    db.insert([card.Card(c).to_hash() for c in content])


def remind():
    cards = [card.load(c) for c in db.read()]
    remind_body = []
    splitter = "\n\n---------------------------------\n\n"
    header = "这是今天要复习的内容：\n\n #################### \n\n"
    for c in cards:
        if c.should_remind():
            remind_body.append(c.content)
            c.round += 1

    db.write([c.to_hash() for c in cards])
    if remind_body:
        m.send(m.config['notifier']['email'], '[Panga] 提醒',
               header + splitter.join(remind_body))


if __name__ == '__main__':
    main()

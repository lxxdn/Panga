from datetime import datetime
from datetime import timedelta

REMIND_INVERVAL = [1, 2, 4, 7, 14, 30, 60, 180, 360]


class Card(object):
    ATTRS = ['content', 'round', 'created_at']
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, content='', round=0, created_at=None):
        self.content = content
        self.round = round
        if not created_at:
            self.created_at = datetime.now().strftime(Card.TIME_FORMAT)

    def to_hash(self):
        return {
            'content': self.content,
            'round': self.round,
            'created_at': self.created_at
        }

    def should_remind(self):
        result = False
        if self.round < len(REMIND_INVERVAL):
            t = datetime.strptime(self.created_at, Card.TIME_FORMAT)
            delta = timedelta(days=REMIND_INVERVAL[self.round])
            result = (t + delta).date() <= datetime.now().date()

        return result


def load(data):
    c = Card()
    if isinstance(data, dict):
        for attr in Card.ATTRS:
            if attr in data:
                setattr(c, attr, data[attr])

    return c


def main():
    card = Card('test')


if __name__ == '__main__':
    main()
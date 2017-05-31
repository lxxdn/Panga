import json
import pdb

class JsonDB(object):
    def __init__(self, db_path='./db.json'):
        self.db_path = db_path

    def read(self):
        with open(self.db_path, 'r') as file:
            content = file.read() or '[]'
            return json.loads(content)

    def write(self, data):
        with open(self.db_path, 'w') as file:
            file.write(json.dumps(data))

def main():
    j = JsonDB('db_test.json')
    j.write({'a': 1, 'b': 2})
    data = j.read()
    print(data)


if __name__ == '__main__':
    main()
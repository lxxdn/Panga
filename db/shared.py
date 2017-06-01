from .json_db import JsonDB

class DB(object):
    def __init__(self, db_instance = None):
        if db_instance == None:
            self.db_instance = JsonDB()
        else:
           self.db_instance = db_instance

    def insert(self, new_data):
        data = self.read()
        if isinstance(new_data, list):
            data = data + new_data
        elif isinstance(new_data, dict):
            data.append(new_data)
        self.db_instance.write(data)

    def write(self, data):
        self.db_instance.write(data)

    def read(self):
        return self.db_instance.read()

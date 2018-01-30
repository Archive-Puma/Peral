import json


class ReadJSON:

    def __init__(self, __dbpath):
        self.database_path = __dbpath

    def read(self):
        try:
            with open(self.database_path, 'r') as db:
                self.content = json.load(db)
        except IOError:
            self.content = None
        return self.content

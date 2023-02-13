import sqlite3


class Database:
    def __init__(self, filename):
        self.base = sqlite3.connect(filename)
        self.cursor = self.base.cursor()
        if self.base:
            print('Database connected!')

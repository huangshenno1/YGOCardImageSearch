import sqlite3
from .card import Card


class CardDatabase:
    def __init__(self, cdb_path):
        self.conn = sqlite3.connect(cdb_path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def query_by_cid(self, cid):
        ret = list(self.cursor.execute(f'select name, desc from texts where id="{cid}" limit 1;'))
        if len(ret) == 0:
            return 'Not Found', ''
        row = ret[0]
        return Card(cid, row[0], row[1])


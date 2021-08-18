import sqlite3
import shlex
import subprocess
import os

DATABASE_PATH = "/home/magic/NJU-Magic/back-end/Data/njumagic_test.db"

class Database():
    def __init__(self, database_path):
        self.database_path = database_path

    def update(self, sql):
        print(sql)
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        cursor = c.execute(sql)

        last_rowid = cursor.lastrowid
        conn.commit()
        conn.close()
        return last_rowid

    def query(self, sql):
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        cursor = c.execute(sql)
        data_row = []
        for row in cursor:
            data_col = []
            for col in row:
                data_col.append(col)

            data_row.append(data_col)
        conn.close()

        return data_row

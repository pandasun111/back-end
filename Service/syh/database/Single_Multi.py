import sqlite3
import shlex
import subprocess
import os
# from ??? import DATABASE_PATH
from datetime import datetime
import shutil
# rebuild_dataset = True
#
# if rebuild_dataset and os.path.exists(DATABASE_PATH):
#        os.remove(DATABASE_PATH)
#
# if not os.path.exists(DATABASE_PATH):
#        subprocess.check_call(
#               shlex.split("sqlite3 {}".format(DATABASE_PATH))
#        )
# else:
#        print("database already exists, skipped")
DATABASE_PATH = "Mutimode.db"
db_file = DATABASE_PATH


def show():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    show_all = 'select * from Single_Multi'
    cur.execute(show_all)
    print(cur.fetchall())
    print("显示完毕")
    conn.commit()
    cur.close()
    conn.close()

def search_sinle_ID(ID):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        sear_id = 'select * from Single_Multi where Single_ID = {}'.format(ID)
        cur.execute(sear_id)
        if cur.fetchall():
            cur.execute(sear_id)
            print(cur.fetchall())
        else:
            print("没有此记录")
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

def search_muti_ID(ID):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        sear_id = 'select * from Single_Multi where Mutimode_ID = {}'.format(ID)
        cur.execute(sear_id)
        if cur.fetchall():
            cur.execute(sear_id)
            print(cur.fetchall())
        else:
            print("没有此记录")
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

def insert(Muti_ID, Sin_ID):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        ins = 'insert into Single_Multi ( Mutimode_ID, Single_ID) ' \
              'values ({}, {})'.\
            format(Muti_ID, Sin_ID)
        cur = conn.cursor()
        cur.execute(ins)
        conn.commit()
        print("插入成功")
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()




#show()
# insert(3,3)
# search_sinle_ID(3)
# search_muti_ID(3)
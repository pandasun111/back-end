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
    show_all = 'select * from Singlemode_Pro'
    cur.execute(show_all)
    print(cur.fetchall())
    print("显示完毕")
    conn.commit()
    cur.close()
    conn.close()



def insert( Sen_ID, Name, Alg, Data):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        ins = 'insert into Singlemode_Pro (  Sensor_ID, Name, Algorithm, Data_Location, Date ) ' \
              'values ("{}","{}","{}","{}","{}")'.\
            format( Sen_ID, Name, Alg, Data, datetime.now())
        cur = conn.cursor()
        cur.execute(ins)
        conn.commit()
        print("插入成功")
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()



def search_ID(ID):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        sear_id = 'select * from Singlemode_Pro where Singlemode_ID = {}'.format(ID)
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



def update(ID, Sen_ID, Name, Alg, Data):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        sear_id = 'select * from Singlemode_Pro where Singlemode_ID = {}'.format(ID)
        cur.execute(sear_id)
        if cur.fetchall():
            upd = 'update Singlemode_Pro set Name = "{}", Sensor_ID = "{}", Data_Location= "{}", ' \
                  'Algorithm = "{}", Date = "{}" where Singlemode_ID = {}'.format(
                Name,  Sen_ID, Data, Alg, datetime.now(), ID)
            cur.execute(upd)
            conn.commit()
            print("修改完成")
        else:
            print("没有此记录")
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()



def delete(ID):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        sear_id = 'select * from Singlemode_Pro where Singlemode_ID = {}'.format(ID)
        cur.execute(sear_id)
        if cur.fetchall():
            dele = 'delete from Singlemode_Pro where Singlemode_ID = {}'.format(ID)
            cur.execute(dele)
            conn.commit()
            print("删除成功")
        else:
            print("没有此记录")
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


# show()
# insert("5","深度图像","四大法算法","D：/asad/1")
# search_ID(3)
#update(1,9,"雷达预测图","sdw法算法","D:/12345/",)
# delete(6)
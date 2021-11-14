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
    show_all = 'select * from Scene_Model'
    cur.execute(show_all)
    print(cur.fetchall())
    print("显示完毕")
    conn.commit()
    cur.close()
    conn.close()



def insert(Name, Type, Data_Loc, Des):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        ins = 'insert into Scene_Model ( Name, Type, Data_Location, Description, Date ) ' \
              'values ("{}","{}","{}","{}","{}")'.\
            format(Name, Type, Data_Loc, Des, datetime.now())
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
        sear_id = 'select * from Scene_Model where Scene_ID = {}'.format(ID)
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



def update(ID, Name, Type, Data_Loc, Des):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        sear_id = 'select * from Scene_Model where Scene_ID = {}'.format(ID)
        cur.execute(sear_id)
        if cur.fetchall():
            upd = 'update Scene_Model set Name = "{}", Type = "{}", Data_Location= "{}", ' \
                  'Description = "{}", Date = "{}" where Scene_ID = {}'.format(
                Name, Type, Data_Loc, Des, datetime.now(), ID)
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
        sear_id = 'select * from Scene_Model where Scene_ID = {}'.format(ID)
        cur.execute(sear_id)
        if cur.fetchall():
            dele = 'delete from Scene_Model where Scene_ID = {}'.format(ID)
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
# insert("苏州地铁","隧道","D:/1234/", "",)
# search_ID(2)
#update(4,"南京地铁","隧道","D:/abc/","完全体",)
# delete(3)
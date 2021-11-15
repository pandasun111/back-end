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
    show_all = 'select * from Multimode_Fus'
    cur.execute(show_all)
    print(cur.fetchall())
    print("显示完毕")
    conn.commit()
    cur.close()
    conn.close()



def insert(Name, Alg, Data_Loc, Des, Sin_ID):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        ins1 = 'insert into Multimode_Fus ( Name, Algorithm, Data_Location, Description, Date ) ' \
              'values ("{}","{}","{}","{}","{}")'.\
            format(Name, Alg, Data_Loc, Des, datetime.now())
        cur.execute(ins1)
        conn.commit()
        last_rowid = cur.lastrowid
        i = 0
        while i <= len(Sin_ID)- 1:
            ins2 = 'insert into Single_Multi (Multimode_ID, Single_ID)' \
               'values ({}, {})'.format(last_rowid, Sin_ID[i])
            cur.execute(ins2)
            conn.commit()
            i = i+ 1
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
        sear_id = 'select * from Multimode_Fus where Multimode_ID = {}'.format(ID)
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



def update(ID, Name, Alg, Data_Loc, Des):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        sear_id = 'select * from Multimode_Fus where Multimode_ID = {}'.format(ID)
        cur.execute(sear_id)
        if cur.fetchall():
            upd = 'update Multimode_Fus set Name = "{}", Algorithm = "{}", Data_Location= "{}", ' \
                  'Description = "{}", Date = "{}" where Multimode_ID = {}'.format(
                Name, Alg, Data_Loc, Des, datetime.now(), ID)
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
        sear_id = 'select * from Multimode_Fus where Multimode_ID = {}'.format(ID)
        cur.execute(sear_id)
        if cur.fetchall():
            dele1 = 'delete from Multimode_Fus where Multimode_ID = {}'.format(ID)
            cur.execute(dele1)
            conn.commit()
            dele2 = 'delete from Single_Multi where Multimode_ID = {}'.format(ID)
            cur.execute(dele2)
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
# insert("雷达图+红外","ravf","D:/1234/","",[1,3,4])
#search_ID(1)
# update(3,"雷达预测","雷达2","D:/12345/","",)
# delete(6)
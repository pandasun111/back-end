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
    show_all = 'select * from Inspection'
    cur.execute(show_all)
    print(cur.fetchall())
    print("显示完毕")
    conn.commit()
    cur.close()
    conn.close()



def insert(Mul_ID, Sce_ID, Name, Alg, Task_Type, Data_Loc):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        ins = 'insert into Inspection ( Multimode_ID, Scene_ID, Name, Algorithm, Task_Type,Data_Location,  Date ) ' \
              'values ("{}","{}","{}","{}","{}","{}","{}")'.\
            format(Mul_ID, Sce_ID, Name, Alg, Task_Type, Data_Loc, datetime.now())
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
        sear_id = 'select * from Inspection where Inspection_ID = {}'.format(ID)
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



def update(ID, Mul_ID, Sce_ID, Name, Alg, Task_Type, Data_Loc):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        sear_id = 'select * from Inspection where Inspection_ID = {}'.format(ID)
        cur.execute(sear_id)
        if cur.fetchall():
            upd = 'update Inspection set Multimode_ID = "{}", Scene_ID = "{}",Name = "{}", ' \
                  'Algorithm = "{}", Task_Type = "{}", Data_Location= "{}", ' \
                  'Date = "{}" where Inspection_ID = {}'.format(
                Mul_ID, Sce_ID, Name, Alg, Task_Type, Data_Loc, datetime.now(), ID)
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
        sear_id = 'select * from Inspection where Inspection_ID = {}'.format(ID)
        cur.execute(sear_id)
        if cur.fetchall():
            dele = 'delete from Inspection where Inspection_ID = {}'.format(ID)
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
# insert(2,4,"南京地铁巡检","orb","隧道巡检","D:/1234/")
# search_ID(2)
#update(1,3,7,"苏州地铁巡检","融合2","隧道巡检","D:/acvf/",)
# delete(2)
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
    show_all = 'select * from Prime_Sense'
    cur.execute(show_all)
    print(cur.fetchall())
    print("显示完毕")
    conn.commit()
    cur.close()
    conn.close()



def insert(Name, Sensor, Data_Loc, Data_Type, Des):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        ins = 'insert into Prime_Sense ( Name, Sensor, Data_Location, Data_Type, Description, Date ) ' \
              'values ("{}","{}","{}","{}","{}","{}")'.\
            format(Name, Sensor, Data_Loc, Data_Type, Des, datetime.now())
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
        sear_id = 'select * from Prime_Sense where Sensor_ID = {}'.format(ID)
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



def update(ID, Name, Sensor, Data_Loc, Data_Type, Des):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        sear_id = 'select * from Prime_Sense where Sensor_ID = {}'.format(ID)
        cur.execute(sear_id)
        if cur.fetchall():
            upd = 'update Prime_Sense set Name = "{}", Sensor = "{}", Data_Location= "{}", ' \
                  'Data_Type = "{}", Description = "{}", Date = "{}" where Sensor_ID = {}'.format(
                Name, Sensor, Data_Loc, Data_Type, Des, datetime.now(), ID)
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
        sear_id = 'select * from Prime_Sense where Sensor_ID = {}'.format(ID)
        cur.execute(sear_id)
        if cur.fetchall():
            dele = 'delete from Prime_Sense where Sensor_ID = {}'.format(ID)
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
#insert("雷达预测","雷达","D:/1234/","视频","",)
#search_ID(76)
#update(9,"雷达预测","雷达2","D:/12345/","图像序列","",)
# delete(5)
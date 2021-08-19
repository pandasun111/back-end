import sqlite3
import shlex
import subprocess
import os

from DAO.dao_utils import DATABASE_PATH
from datetime import datetime
import shutil

rebuild_dataset = True

if rebuild_dataset and os.path.exists(DATABASE_PATH):
       os.remove(DATABASE_PATH)

if not os.path.exists(DATABASE_PATH):
       subprocess.check_call(
              shlex.split("sqlite3 {}".format(DATABASE_PATH))
       )
else:
       print("database already exists, skipped")

conn = sqlite3.connect(DATABASE_PATH)
c = conn.cursor()

try:
       c.execute("CREATE TABLE SensorData \
              (sensor_data_id INTEGER PRIMARY KEY AUTOINCREMENT,\
              sensor_rgb_path           CHAR(50)    ,\
              sensor_depth_path            CHAR(50)  ,\
              sensor_lidar_path        CHAR(50),\
              sensor_data_path         CHAR(50),\
              upload_date              CHAR(50),\
              sensor_data_cover        CHAR(50));"
              )

       conn.commit()
except Exception as e:
       print(str(e))
       #print("table SensorData has already exists, skipped")


try:
       c.execute("CREATE TABLE AlgorithmRes \
              (algorithm_res_id INTEGER PRIMARY KEY  AUTOINCREMENT,\
              sensor_data_id           INT    ,\
              algorithm_type            INT  ,\
              algorithm_name        CHAR(50),\
              algorithm_result         CHAR(50));"
                 )

       conn.commit()
except Exception as e:
       print(str(e))
       #print("table AlgorithmRes has already exists, skipped")


real_path = os.path.dirname(os.path.realpath(__file__))


try:
       cursor = c.execute("insert into SensorData (sensor_rgb_path, \
                                              sensor_depth_path,\
                                              sensor_lidar_path, \
                                              sensor_data_path, \
                                              upload_date, \
                                              sensor_data_cover) values\
                                              ('{}', '{}', '{}', '{}', '{}', '{}')".format(
              "/Data/demo/rgb.mp4",
              "/Data/demo/depth.mp4",
              "",
              "/Data/demo/raw.h5",
              datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S'),
              "/Data/demo/cover.png"))

       conn.commit()
       last_rowid = cursor.lastrowid
       print("successfully init demo sensor data, rowid={}".format(last_rowid))
except Exception as e:
       last_rowid = None
       print(str(e))

if last_rowid is not None:
       try:
              c.execute("insert into AlgorithmRes (sensor_data_id, \
                                                     algorithm_type,\
                                                     algorithm_name, \
                                                     algorithm_result) values\
                                                     ({}, {}, '{}', '{}')".format(
                     last_rowid,
                     0,
                     "rgb_recon",
                     "/Data/demo/rgb_reconstruction.ply"))
              conn.commit()
       except Exception as e:
              print(str(e))

       try:
              c.execute("insert into AlgorithmRes (sensor_data_id, \
                                                     algorithm_type,\
                                                     algorithm_name, \
                                                     algorithm_result) values\
                                                     ({}, {}, '{}', '{}')".format(
                     last_rowid,
                     1,
                     "depth_recon",
                     "/Data/demo/depth_reconstruction.ply"))
              conn.commit()
       except Exception as e:
              print(str(e))

       try:
              c.execute("insert into AlgorithmRes (sensor_data_id, \
                                                     algorithm_type,\
                                                     algorithm_name, \
                                                     algorithm_result) values\
                                                     ({}, {}, '{}', '{}')".format(
                     last_rowid,
                     2,
                     "rgb_semantic",
                     "/Data/demo/rgb_semantic.ply"))
              conn.commit()
       except Exception as e:
              print(str(e))

       try:
              c.execute("insert into AlgorithmRes (sensor_data_id, \
                                                     algorithm_type,\
                                                     algorithm_name, \
                                                     algorithm_result) values\
                                                     ({}, {}, '{}', '{}')".format(
                     last_rowid,
                     3,
                     "rgb_recon",
                     "/Data/demo/depth_semantic.ply"))
              conn.commit()
       except Exception as e:
              print(str(e))

conn.close()
import sqlite3
import shlex
import subprocess
import os
from DAO.dao_utils import DATABASE_PATH
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
              algorithm_type            CHAR(50)  ,\
              algorithm_name        CHAR(50),\
              algorithm_result         CHAR(50));"
                 )

       conn.commit()
except Exception as e:
       print(str(e))
       #print("table AlgorithmRes has already exists, skipped")

conn.close()
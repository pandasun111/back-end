import sqlite3

db_file = "Mutimode.db"

conn = sqlite3.connect(db_file)


# search = 'select * from Prime_Sense'
def insert_data():
    ins = 'insert into Prime_Sense ( Name, Sensor, Data_Location, Data_Type, Description, Date ) ' \
          'values (?,?,?,?,?,?)'
    data = ("红外光", "红外摄像头", "E:/abc/", "图片","", "2021111111160405"  )
    cur = conn.cursor()
    cur.execute(ins, data)
    conn.commit()
    cur.close()
    conn.close()


# insert_data()
# print(cur.fetchall())
# conn.close()
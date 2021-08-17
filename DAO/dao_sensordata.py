from DAO.dao_utils import *

def addSensorData(rgb_stream, depth_stream, lidar_stream, sensor_data, upload_date, sensor_data_cover):
    '''
    params:
    rgb_stream        type:str
    depth_stream      type:str
    lidar_stream      type:str
    sensor_data       type:str
    upload_date       type:str
    sensor_data_cover type:str
    '''
    assert type(rgb_stream) == str, "rgb_stream should be the path of rgb video"
    assert type(depth_stream) == str, "depth_stream should be the path of rgb video"
    assert type(lidar_stream) == str, "lidar_stream should be the path of rgb video"
    assert type(sensor_data) == str, "sensor_data should be the path of rgb video"

    database = Database(DATABASE_PATH)

    database.update("insert into SensorData (sensor_rgb_path, \
                                              sensor_depth_path,\
                                              sensor_lidar_path, \
                                              sensor_data_path, \
                                              upload_date, \
                                              sensor_data_cover) values\
                                              ('{}', '{}', '{}', '{}', '{}', '{}')".format(
                                            rgb_stream,
                                            depth_stream,
                                            lidar_stream,
                                            sensor_data,
                                            upload_date,
                                            sensor_data_cover))

def querySensorData():
    '''
    returns:
    data    type:list
    '''
    database = Database(DATABASE_PATH)

    cursor = database.query("select sensor_data_id, upload_date, sensor_data_cover from SensorData")

    data = []
    for row in cursor:
        data.append({
            "sensor_data_id" : row[0],
            "upload_date": row[1],
            "sensor_data_cover": row[2]
        })

    return data

def querySensorDataByID(sensor_data_id):
    '''
    params:
    sensor_data_id      type:int
    returns:
    data                type:dict
    '''
    database = Database(DATABASE_PATH)

    cursor = database.query("select * from SensorData where sensor_data_id={}".format(sensor_data_id))

    row = cursor[0]

    data = {
            "sensor_data_id" : row[0],
            "sensor_rgb_path" : row[1],
            "sensor_depth_path" : row[2],
            "sensor_lidar_path" : row[3],
            "upload_date": row[5],
            "sensor_data_cover": row[6]
        }

    return data

import requests
from flask_cors import *
from flask import Flask, render_template, Response
import threading
import time
from flask import request
from flask import jsonify
app = Flask(__name__)
CORS(app, supports_credentials=True)

import os
import cv2
import math
import h5py
import subprocess
import numpy as np
import open3d as o3d
from datetime import datetime
from skimage.color import label2rgb
from Service.wy.api_wang import reconstruct_from_rgb, pose_estimation_from_rgb
from Service.lhw.api_liu import reconstruct_from_depth
from Service.lhw.src.fusion_depth import meshwrite_color
from Service.lst.api_lst import api_semantic_segmentation
from DAO.dao_sensordata import addSensorData
from DAO.dao_algorithm import addAlgorithmResData
# TODO: import DAO class and function

# store all data received in one operation
received_data = []

class DownThread:
    def __init__(self):
        self._running = False
        self.url = None

    def start(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        while True:
            if self._running:
                global received_data
                url = "http://172.27.142.89:5000/upload_sensor_data"
                res = requests.post(url=url,data={})
                #print(res.text)
                received_data.append(res.text)
                time.sleep(0.1)

download_sensor_data = DownThread()
download_sensor_data_thread = threading.Thread(target=download_sensor_data.run)
download_sensor_data_thread.start()

@app.route('/startrecording', methods=['POST'])
@cross_origin()
def startrecording():
    url = request.get_json()['url']
    download_sensor_data.url = url
    download_sensor_data.start()
    return jsonify({})


@app.route('/endrecording', methods=['POST'])
@cross_origin()
def endrecording():
    download_sensor_data.terminate()
    process_sensor_data()
    return jsonify({})

def process_sensor_data():
    # process and store sensor data
    global received_data
    print(len(received_data))
    if len(received_data) == 0:
        return

    # create folder of sensor data
    date = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/Data/" + date
    isExists = os.path.exists(dir_path)
    if not isExists:
        os.makedirs(dir_path)
    dir_path = dir_path + "/"

    # use first frame as a sample data
    sample_data = received_data[0].replace("null", "None")
    sample_data = eval(sample_data) # get 'dict' type data

    # video frame list and VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # rgb video param
    rgb_frame_list = []
    rgb_frame_size = sample_data["rgb_size"]
    rgb_video_path = [dir_path + "rgb_video.avi", dir_path + "rgb_video.mp4"]
    rgb_videoWriter = cv2.VideoWriter(rgb_video_path[0], fourcc, 30, (rgb_frame_size[1], rgb_frame_size[0]))
    # depth video param
    if sample_data["depth_raw"] is None:
        depth_isExist = False
    else:
        depth_isExist = True
        depth_frame_list = []
        depth_frame_size = sample_data["depth_size"]
        depth_video_path = [dir_path + "depth_video.avi", dir_path + "depth_video.mp4"]
        depth_videoWriter = cv2.VideoWriter(depth_video_path[0], fourcc, 30, (depth_frame_size[1], depth_frame_size[0]))
    # lidar video param
    if sample_data["lidar_raw"] is None:
        lidar_isExist = False
    else:
        lidar_isExist = True
        lidar_frame_list = []
        lidar_frame_size = [600, 600]
        lidar_video_path = [dir_path + "lidar_video.avi", dir_path + "lidar_video.mp4"]
        lidar_videoWriter = cv2.VideoWriter(lidar_video_path[0], fourcc, 30, (lidar_frame_size[1], lidar_frame_size[0]))

    # save cover for this sensor data
    cover_path = dir_path + "cover.jpg"
    cover = np.array(sample_data["rgb_frame"], dtype=np.uint8)
    cover = cover.reshape((rgb_frame_size[0], rgb_frame_size[1], 3))
    cover = cv2.cvtColor(cover, cv2.COLOR_RGB2BGR) # opencv use BGR channel
    cv2.imwrite(cover_path, cover)

    for data in received_data:
        data = data.replace("null", "None")
        data = eval(data) # get 'dict' type data

        # write rgb video
        rgb_frame = np.array(data["rgb_frame"], dtype=np.uint8)
        rgb_frame = rgb_frame.reshape((rgb_frame_size[0], rgb_frame_size[1], 3))
        rgb_frame_list.append(rgb_frame)
        bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR) # opencv use BGR channel
        rgb_videoWriter.write(bgr_frame)

        # write depth video
        if depth_isExist:
            uint8_depth_frame = np.array(data["depth_raw"], dtype=np.uint8)
            depth_frame = uint8_depth_frame.view('<f4')
            depth_frame[np.isnan(depth_frame)] = 0
            depth_frame_list.append(depth_frame)
            r = np.max(depth_frame) - np.min(depth_frame)
            if r != 0:
                depth_frame = (depth_frame - np.min(depth_frame)) / r * 255
            else:
                depth_frame = np.zeros((depth_frame_size[0], depth_frame_size[1]))
            depth_frame = depth_frame.astype(np.uint8)
            depth_frame = cv2.applyColorMap(depth_frame,cv2.COLORMAP_JET)
            depth_videoWriter.write(depth_frame)

        # write lidar video
        if lidar_isExist:
            lidar_frame = np.zeros((600, 600,3), np.uint8)
            angle = data["lidar_angle_min"]
            for r in data["lidar_ranges"]:
                if math.isinf(r) == True:
                    r = 0
                x = math.trunc((r * 50.0)*math.cos(angle + (-90.0*3.1416/180.0)))
                y = math.trunc((r * 50.0)*math.sin(angle + (-90.0*3.1416/180.0)))
                #set the borders (all values outside the defined area should be 0)
                if y > 600 or y < -600 or x<-600 or x>600:
                    x=0
                    y=0
                cv2.line(lidar_frame,(300, 300),(x+300,y+300),(255,0,0),2)
                angle= angle + data["lidar_angle_increment"] 
            cv2.circle(lidar_frame, (300, 300), 2, (255, 255, 0))
            lidar_videoWriter.write(lidar_frame)

    # write video and change to h264 mp4
    devNull = open(os.devnull, 'w')
    rgb_videoWriter.release()
    cmd = 'ffmpeg -y -i {} -vcodec h264 {} && rm {}'.format(rgb_video_path[0], rgb_video_path[1], rgb_video_path[0])
    subprocess.Popen(cmd, stdout=devNull)
    depth_videoWriter.release()
    cmd = 'ffmpeg -y -i {} -vcodec h264 {} && rm {}'.format(depth_video_path[0], depth_video_path[1], depth_video_path[0])
    subprocess.Popen(cmd, stdout=devNull)
    lidar_videoWriter.release()
    cmd = 'ffmpeg -y -i {} -vcodec h264 {} && rm {}'.format(lidar_video_path[0], lidar_video_path[1], lidar_video_path[0])
    subprocess.Popen(cmd, stdout=devNull)

    # use rgb frames to estimate pose
    poses = pose_estimation_from_rgb(rgb_frame_list, np.array(sample_data["rgb_intrin"]))
    
    # add pose to sensor data
    for i, data in enumerate(received_data):
        data["pose"] = poses[i]
    
    # write data into h5 file
    h5_path = dir_path + "sensor_data.h5"
    h5_file = h5py.File(h5_path, 'w')
    for i, data in enumerate(received_data):
        grp = h5_file.create_group(str(i))
        for key, value in data:
            if value is None:
                grp[key] = np.nan
            else:
                grp[key] = value
    h5_file.close()

    # rgb reconstruction
    rgb_recon = reconstruct_from_rgb(rgb_frame_list, poses, np.array(sample_data["rgb_intrin"]))
    rgb_recon_path = dir_path + "rgb_reconstruction.ply"
    rgb_recon.export(rgb_recon_path)

    # depth reconstrunction
    if depth_isExist:
        vertices, triangles, colors = reconstruct_from_depth(depth_frame_list, poses, np.array(sample_data["depth_intrin"]), rgb_frame_list)
        depth_recon_path = dir_path + "depth_reconstruction.ply"
        meshwrite_color(depth_recon_path, vertices, triangles, colors)

    # rgb semantic segmentation
    rgb_sem_seg_path = dir_path + "rgb_semantic_segmentation.ply"
    pcs = o3d.io.read_point_cloud(rgb_recon_path)
    pcs.estimate_normals()
    points = pcs.points
    colors = pcs.colors
    normals = pcs.normals
    pcs = np.concatenate([points, colors, normals], axis=1)
    label = api_semantic_segmentation(pcs)
    colors = [np.random.uniform(0,1,(3)) for _ in range(13)]
    xyz = pcs[:, 6:9]
    rgb = label2rgb(np.array(label), colors = colors)
    ppc = o3d.geometry.PointCloud()
    ppc.points = o3d.utility.Vector3dVector(xyz)
    ppc.colors = o3d.utility.Vector3dVector(rgb)
    o3d.io.write_point_cloud(rgb_sem_seg_path, ppc)

    # depth semantic segmentation 
    if depth_isExist:
        depth_sem_seg_path = dir_path + "depth_semantic_segmentation.ply"
        pcs = o3d.io.read_point_cloud(depth_recon_path)
        pcs.estimate_normals()
        points = pcs.points
        colors = pcs.colors
        normals = pcs.normals
        pcs = np.concatenate([points, colors, normals], axis=1)
        label = api_semantic_segmentation(pcs)
        colors = [np.random.uniform(0,1,(3)) for _ in range(13)]
        xyz = pcs[:, 6:9]
        rgb = label2rgb(np.array(label), colors = colors)
        ppc = o3d.geometry.PointCloud()
        ppc.points = o3d.utility.Vector3dVector(xyz)
        ppc.colors = o3d.utility.Vector3dVector(rgb)
        o3d.io.write_point_cloud(depth_sem_seg_path, ppc)

    # write all url to dataset
    sensor_data_id = addSensorData(rgb_video_path[1], depth_video_path[1], lidar_video_path[1], h5_path, date, cover_path)
    addAlgorithmResData(sensor_data_id, 0, "rgb_reconstruction", rgb_recon_path)
    addAlgorithmResData(sensor_data_id, 2, "rgb_semantic_segmentation", rgb_sem_seg_path)
    if depth_isExist:
        addAlgorithmResData(sensor_data_id, 1, "depth_reconstruction", depth_recon_path)
        addAlgorithmResData(sensor_data_id, 3, "depth_semantic_segmentation", depth_sem_seg_path)

    received_data.clear()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000 ,debug=True)
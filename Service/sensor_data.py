import glob
import threading

import numpy as np
import requests
import os
from datetime import datetime
import time
import json
import cv2
from DAO.dao_algorithm import *
from DAO.dao_sensordata import *
from Service.video_utils import depth_raw2_rgb
import h5py
import subprocess
import open3d as o3d
from datetime import datetime
from skimage.color import label2rgb
from Service.wy.api_wang import reconstruct_from_rgb, pose_estimation_from_rgb
from Service.lhw.api_liu import reconstruct_from_depth
from Service.lhw.src.fusion_depth import meshwrite_color
from Service.lst.api_lst import api_semantic_segmentation
from DAO.dao_sensordata import addSensorData
from DAO.dao_algorithm import addAlgorithmResData
import torch
import math
import subprocess
import h5py

class SensorDownloader:
    def __init__(self):
        self._running = False
        self.url = ""
        self.saving_folder = None


    def start(self):
        self._running = True
        self.saving_folder = os.path.dirname(os.path.realpath(__file__)) + "/../Data/" + datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
        if not os.path.exists(self.saving_folder):
            os.makedirs(self.saving_folder)

    def terminate(self):
        self._running = False

    def run(self):
        while True:
            if self._running:
                try:
                    print("send requests")
                    res = requests.post(url=self.url,data={})
                    raw_data = res.json()
                    raw_data_save_path = os.path.join(self.saving_folder, "raw")
                    if not os.path.exists(raw_data_save_path):
                        os.makedirs(raw_data_save_path)
                    torch.save(raw_data, os.path.join(raw_data_save_path, "{}.pth".format(time.time())))
                except Exception as e:
                    print(str(e))

                '''
                img = cv2.imdecode(np.array(raw_data["rgb_frame"], dtype=np.uint8), cv2.IMREAD_COLOR)
                if raw_data["depth_raw"] != "null":
                    depth = cv2.imdecode(np.asarray(raw_data["depth_raw"], dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                    depth = depth_raw2_rgb(depth)
                
                cv2.imshow("rgb", img)

                cv2.imshow("depth", depth)
                key = cv2.waitKey(1) & 0xFF
                time.sleep(1)
                '''

def process_sensor_data(recived_data_folder):
    received_data = [
        torch.load(f) for f in glob.glob(os.path.join(recived_data_folder, "*.pth"))
    ]
    if len(received_data) == 0:
        return

    # create folder of sensor data
    date = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/Data/" + date
    isExists = os.path.exists(dir_path)
    if not isExists:
        os.makedirs(dir_path)
    dir_path = dir_path + "/"
    dataset_path = "/Data/" + date + "/"

    # use first frame as a sample data
    sample_data = received_data[0] # get 'dict' type data

    # video frame list and VideoWriter
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    fps = 2
    # rgb video param
    rgb_frame_list = []
    rgb_frame_size = sample_data["rgb_size"]
    rgb_video_path = [dir_path + "rgb_video.avi", dir_path + "rgb_video.mp4", dataset_path + "rgb_video.mp4"]
    rgb_videoWriter = cv2.VideoWriter(rgb_video_path[0], fourcc, fps, (rgb_frame_size[1], rgb_frame_size[0]))
    print(rgb_video_path[0])
    print(rgb_videoWriter.isOpened())
    # depth video param
    if sample_data["depth_raw"] is None:
        depth_isExist = False
        depth_video_path = ["", "", ""]
    else:
        depth_isExist = True
        depth_frame_list = []
        depth_frame_size = sample_data["depth_size"]
        depth_video_path = [dir_path + "depth_video.avi", dir_path + "depth_video.mp4", dataset_path + "depth_video.mp4"]
        depth_videoWriter = cv2.VideoWriter(depth_video_path[0], fourcc, fps, (depth_frame_size[1], depth_frame_size[0]))
    print("depth_isExist", depth_isExist)
    # lidar video param
    if sample_data["lidar_raw_seq"] is None:
        lidar_isExist = False
        lidar_video_path = ["", "", ""]
    else:
        lidar_isExist = True
        lidar_frame_size = [600, 600]
        lidar_video_path = [dir_path + "lidar_video.avi", dir_path + "lidar_video.mp4", dataset_path + "lidar_video.mp4"]
        lidar_videoWriter = cv2.VideoWriter(lidar_video_path[0], fourcc, fps, (lidar_frame_size[1], lidar_frame_size[0]))

    # save cover for this sensor data

    cover_path = dir_path + "cover.jpg"
    cover = np.array(sample_data["rgb_frame"], dtype=np.uint8)
    cover = cv2.imdecode(cover, cv2.IMREAD_COLOR)
    #cover = cv2.cvtColor(cover, cv2.COLOR_RGB2BGR) # opencv use BGR channel
    cv2.imwrite(cover_path, cover)


    for data in received_data:
        # write rgb video
        rgb_frame = np.array(data["rgb_frame"], dtype=np.uint8)
        rgb_frame = cv2.imdecode(rgb_frame, cv2.IMREAD_COLOR)
        print(rgb_frame.dtype)
        rgb_frame_list.append(rgb_frame)
        #bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR) # opencv use BGR channel
        rgb_videoWriter.write(rgb_frame)

        # write depth video
        if depth_isExist:
            depth = cv2.imdecode(np.asarray(data["depth_raw"], dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            depth_frame = depth_raw2_rgb(depth)
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
    cmd = 'ffmpeg -y -i {} -vcodec h264 {}'.format(rgb_video_path[0], rgb_video_path[1])
    subprocess.call(cmd, shell=True)
    if depth_isExist:
        depth_videoWriter.release()
        cmd = 'ffmpeg -y -i {} -vcodec h264 {}'.format(depth_video_path[0], depth_video_path[1])
        subprocess.call(cmd, shell=True)
    if lidar_isExist:
        lidar_videoWriter.release()
        cmd = 'ffmpeg -y -i {} -vcodec h264 {}'.format(lidar_video_path[0], lidar_video_path[1])
        subprocess.call(cmd, shell=True)

    # # use rgb frames to estimate pose
    print("start estimate pose")
    poses = pose_estimation_from_rgb(rgb_frame_list, np.array(sample_data["rgb_intrin"]))
    print("end estimate pose")

    # # add pose to sensor data
    for i, data in enumerate(received_data):
        data["pose"] = poses[i]

    # write data into h5 file
    print("start write h5")
    h5_path = dir_path + "sensor_data.h5"
    h5_file = h5py.File(h5_path, 'w')
    for i, data in enumerate(received_data):
        grp = h5_file.create_group("frame_" + str(i))
        for key, value in data.items():
            if value is None:
                grp[key] = np.nan
            elif type(value) is dict:
                ggrp = grp.create_group(key)
                for k, v in value.items():
                    ggrp[k] = v
            else:
                grp[key] = value
    h5_file.close()
    print("end write h5")

    # # rgb reconstruction
    rgb_recon = reconstruct_from_rgb(rgb_frame_list, poses, np.array(sample_data["rgb_intrin"]))
    rgb_recon_path = dir_path + "rgb_reconstruction.ply"
    rgb_recon_dataset_path = dataset_path + "rgb_reconstruction.ply"
    rgb_recon.export(rgb_recon_path)

    # # depth reconstrunction
    if depth_isExist:
        print(sample_data["depth_intrin"])
        vertices, triangles, colors = reconstruct_from_depth(depth_frame_list, poses, np.array(sample_data["depth_intrin"]), rgb_frame_list)
        depth_recon_path = dir_path + "depth_reconstruction.ply"
        depth_recon_dataset_path = dataset_path + "depth_reconstruction.ply"
        meshwrite_color(depth_recon_path, vertices, triangles, colors)

    # # rgb semantic segmentation
    rgb_sem_seg_path = dir_path + "rgb_semantic_segmentation.ply"
    rgb_sem_seg_dataset_path = dataset_path + "rgb_semantic_segmentation.ply"
    pcs = o3d.io.read_point_cloud(rgb_recon_path)
    pcs.estimate_normals()
    points = pcs.points
    colors = pcs.colors
    normals = pcs.normals
    if len(pcs.points) != 0:
        pcs = np.concatenate([normals, colors, points], axis=1)
        label = api_semantic_segmentation(pcs)
        colors = [np.random.uniform(0,1,(3)) for _ in range(13)]
        xyz = pcs[:, 6:9]
        rgb = label2rgb(np.array(label), colors = colors)
        ppc = o3d.geometry.PointCloud()
        ppc.points = o3d.utility.Vector3dVector(xyz)
        ppc.colors = o3d.utility.Vector3dVector(rgb)
        o3d.io.write_point_cloud(rgb_sem_seg_path, ppc)
    else:
        rgb_sem_seg_dataset_path = ""
    

    # # depth semantic segmentation
    if depth_isExist:
        depth_sem_seg_path = dir_path + "depth_semantic_segmentation.ply"
        depth_sem_seg_dataset_path = dataset_path + "depth_semantic_segmentation.ply"
        pcs = o3d.io.read_point_cloud(depth_recon_path)
        pcs.estimate_normals()
        points = pcs.points
        colors = pcs.colors
        normals = pcs.normals
        if len(pcs.points) != 0:
            pcs = np.concatenate([normals, colors, points], axis=1)
            label = api_semantic_segmentation(pcs)
            colors = [np.random.uniform(0,1,(3)) for _ in range(13)]
            xyz = pcs[:, 6:9]
            rgb = label2rgb(np.array(label), colors = colors)
            ppc = o3d.geometry.PointCloud()
            ppc.points = o3d.utility.Vector3dVector(xyz)
            ppc.colors = o3d.utility.Vector3dVector(rgb)
            o3d.io.write_point_cloud(depth_sem_seg_path, ppc)
        else:
            depth_sem_seg_dataset_path = ""

    # write all url to dataset
    sensor_data_id = addSensorData(rgb_video_path[2], depth_video_path[2], lidar_video_path[2], dataset_path + "sensor_data.h5", date, dataset_path + "cover.jpg")
    addAlgorithmResData(sensor_data_id, 0, "rgb_reconstruction", rgb_recon_dataset_path)
    addAlgorithmResData(sensor_data_id, 2, "rgb_semantic_segmentation", rgb_sem_seg_dataset_path)
    if depth_isExist:
        addAlgorithmResData(sensor_data_id, 1, "depth_reconstruction", depth_recon_dataset_path)
        addAlgorithmResData(sensor_data_id, 3, "depth_semantic_segmentation", depth_sem_seg_dataset_path)



if __name__ == '__main__':
    folder = r"/home/magic/NJU-Magic/back-end/Data/2021-08-19-22-20-15/raw"
    process_sensor_data(folder)
    '''
    import threading

    download_sensor_data = SensorDownloader("http://172.27.142.89:5000/upload_sensor_data")
    download_sensor_data_thread = threading.Thread(target=download_sensor_data.run)
    download_sensor_data_thread.start()

    while True:
        i = input()
        if i == "s":
            download_sensor_data.start()
        if i == "e":
            download_sensor_data.terminate()
    '''
    #m = torch.load(r"F:\MagicScenePercep1\back-end\Data\2021-08-19-18-45-34\raw\1629369934.8447022.pth")["rgb_frame"]
    #cover = np.array(m, dtype=np.uint8)
    #cover = cv2.imdecode(cover, cv2.IMREAD_COLOR)
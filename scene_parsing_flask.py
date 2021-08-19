import requests
from flask_cors import *
from flask import Flask, render_template, Response
import threading
import time
from flask import request
from flask import jsonify

from DAO.dao_sensordata import *
from DAO.dao_algorithm import *

app = Flask(__name__, static_folder='./Data')
CORS(app, supports_credentials=True)


@app.route('/getallsceneinfo', methods=['POST'])
@cross_origin()
def getallsceneinfo():
    data = querySensorData()

    res = []
    for d in data:
        res.append({
            "sceneId": d["sensor_data_id"],
            "title": "Scene {}".format(d["sensor_data_id"]),
            "description": d["upload_date"]
        })

    return jsonify({"res": res})


@app.route('/getsceneinfobyid', methods=['POST'])
@cross_origin()
def getsceneinfobyid():
    sceneId = request.get_json()['sceneId']

    scene_info = querySensorDataByID(sceneId)
    url = "http://114.212.81.162:4001"
    res = {
        "scene_name": "Scene",
        "scene_scan_date": scene_info["upload_date"],
        "scene_video_length": "00:30:00",
        "scene_type": "indoor",
        "scene_clutter_num": 30,
        "scene_rgb_url": url + scene_info["sensor_rgb_path"],
        "scene_depth_url": url + scene_info["sensor_depth_path"],
        "scene_lidar_url": url + scene_info["sensor_lidar_path"],
        "scene_rgb_recon_url": "http://114.212.81.162:4001/Data/Test/rgb.ply",
        "scene_depth_recon_url": "http://114.212.81.162:4001/Data/Test/seman_rgb.ply",
        "scene_semantic_rgb_recon_url": "http://114.212.81.162:4001/Data/Test/rgb.ply",
        "scene_semantic_depth_recon_url": "http://114.212.81.162:4001/Data/Test/seman_rgb.ply"
    }

    alg_res = queryAlgorithmBySensorId(sceneId)

    for ar in alg_res:
        if int(ar["algorithm_type"]) == 0:
            res["scene_rgb_recon_url"] = url + ar["algorithm_result"]
        elif int(ar["algorithm_type"]) == 1:
            res["scene_depth_recon_url"] = url + ar["algorithm_result"]
        elif int(ar["algorithm_type"]) == 2:
            res["scene_semantic_rgb_recon_url"] = url + ar["algorithm_result"]
        elif int(ar["algorithm_type"]) == 3:
            res["scene_semantic_depth_recon_url"] = url + ar["algorithm_result"]


    return jsonify({"res": res})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001, debug=True)

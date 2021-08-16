import requests
from flask_cors import *
from flask import Flask, render_template, Response
import threading
import time
from flask import request
from flask import jsonify
app = Flask(__name__, static_folder='./Data')
CORS(app, supports_credentials=True)

@app.route('/getallsceneinfo', methods=['POST'])
@cross_origin()
def getallsceneinfo():
    res = []
    for i in range(10):
    	res.append({"title": "Scene_0010", "description": "2021-06-24"})

    return jsonify({"res": res})

@app.route('/getsceneinfobyid', methods=['POST'])
@cross_origin()
def getsceneinfobyid():
	res = {
		"scene_name": "Scene_0010",
		"scene_scan_date": time.time(),
		"scene_video_length": "00:30:00",
		"scene_type": "indoor",
		"scene_clutter_num": 30,
		"scene_rgb_url": "http://114.212.81.162:4001/Data/Test/t1.mp4",
		"scene_depth_url": "http://114.212.81.162:4001/Data/Test/t1.mp4",
		"scene_lidar_url": "http://114.212.81.162:4001/Data/Test/t1.mp4",
		"scene_rgb_recon_url": "http://114.212.81.162:4001/Data/Test/rgb.ply",
		"scene_depth_recon_url": "http://114.212.81.162:4001/Data/Test/seman_rgb.ply",
		"scene_semantic_rgb_recon_url": "http://114.212.81.162:4001/Data/Test/rgb.ply",
		"scene_semantic_depth_recon_url": "http://114.212.81.162:4001/Data/Test/seman_rgb.ply"
	}
	return jsonify({"res": res})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001 ,debug=True)
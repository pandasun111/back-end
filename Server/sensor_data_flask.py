import requests
from flask_cors import *
from flask import Flask, render_template, Response
import threading
import time
from flask import request
from flask import jsonify
from Service.sensor_data import SensorDownloader, process_sensor_data
app = Flask(__name__)
CORS(app, supports_credentials=True)
import shutil
sensor_data_downloader = SensorDownloader()
download_sensor_data_thread = threading.Thread(target=sensor_data_downloader.run)
download_sensor_data_thread.start()

@app.route('/startrecording', methods=['POST'])
@cross_origin()
def startrecording():
    url = request.get_json()['url'] + "/upload_sensor_data"
    sensor_data_downloader.url = url
    sensor_data_downloader.start()
    return jsonify({})


@app.route('/endrecording', methods=['POST'])
@cross_origin()
def endrecording():
    sensor_data_downloader.terminate()
    time.sleep(1)
    process_sensor_data(sensor_data_downloader.saving_folder + "/raw")
    shutil.rmtree(sensor_data_downloader.saving_folder)
    return jsonify({})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000 ,debug=True)
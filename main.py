import requests
from flask_cors import *
from flask import Flask, render_template, Response
import threading
import time
from flask import request
from flask import jsonify
app = Flask(__name__)
CORS(app, supports_credentials=True)


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
                url = "http://172.27.142.89:5000/upload_sensor_data"
                res = requests.post(url=url,data={})
                print(res.text)
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
    return jsonify({})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000 ,debug=True)
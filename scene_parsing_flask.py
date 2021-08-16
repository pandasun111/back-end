import requests
from flask_cors import *
from flask import Flask, render_template, Response
import threading
import time
from flask import request
from flask import jsonify
app = Flask(__name__)
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
	pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001 ,debug=True)
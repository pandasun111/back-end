import requests
from flask_cors import *
from flask import Flask, render_template, Response
from flask import request
from flask import jsonify
from psgn import main

app = Flask(__name__)
CORS(app, supports_credentials=True) # 允许跨域

# 定义你的服务接口，接口名为api1（接口名你自己设定），请求方式为POST（POST方式不要改）
@app.route('/api1', methods=['POST'])
@cross_origin() # 这句话一定要加上，允许跨域
def api1():
	## 这里举一个例子，例如，我输入的是一段视频，输出是一个三维模型，那么，我会告诉你视频地址在哪，然后，你将三维模型存储在文件里，返回给我三维模型文件地址
    image_path = request.get_json()['image_path']
    
    try:
		# 这里开始写你的算法，例如
		model_path = reconstruct(image_path) # 重建并返回结果地址
		
		# 返回结果至前端，包括处理是否成功 success字段，以及你的结果字段 model_path
		return jsonify({
			"sucess": 1,
			"model_path": model_path
			})
    except Exception, e:
		# 捕获异常，例如你的算法中间出错了，出错信息要提示

		# 返回异常信息， 包括处理失败字段success 0，以及错误信息 error_info
		return jsonify({
			"sucess": 0,
			"error_info": str(e)
			})
if __name__ == '__main__':
	# 你自己定义端口，port=4001等，其余不要动
    app.run(host='0.0.0.0', port=4010 ,debug=True)

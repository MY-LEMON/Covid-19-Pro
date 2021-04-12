from flask import Flask, render_template,jsonify,request
import json
import re
import rsa
import base64
import time
import random

"""
接口说明：
1.返回的是json数据
2.结构如下
{
    resCode： 0, # 非0即错误 1
    data： # 数据位置，一般为数组
    message： '对本次请求的说明'
}
"""

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.errorhandler(404)
def handler_404_error(err):
    resData = {
        "resCode": 404,
        "data": [],
        "message": err
    }
    return jsonify(resData)

# 主页面
@app.route('/', methods=['GET','POST'])
def aaa():
    return 'hello'

@app.route('/index')
def bbb():
    return jsonify('world', methods=['POST'])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1943, debug=True)

from flask import Flask, render_template, jsonify, request
import json
import re
import rsa
import base64
import time
import random
from QAmain import KGQA

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

# 检查是否含有特殊字符
def is_string_validate(str):
    sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",str)
    if len(str) == len(sub_str):
        # 说明合法
        return False
    else:
        # 不合法
        return True


@app.errorhandler(404)
def handler_404_error(err):
    resData = {
        "resCode": 404,
        "data": [],
        "message": err
    }
    return jsonify(resData)


# 主页面
@app.route('/', methods=['GET', 'POST'])
def aaa():
    return 'hello'


@app.route('/index')
def bbb():
    return jsonify('world', methods=['POST'])


@app.route('/search', methods=['POST'])
def search_kg():
    if request.method == 'POST':
        get_data = json.loads(request.get_data(as_text=True))
        key = get_data['key']
        print(key)
        if is_string_validate(key):
            resData = {
                "resCode": 1,  # 非0即错误 1
                "data": [],  # 数据位置，一般为数组
                "message": '参数错误'
            }
            return jsonify(resData)

        handler = KGQA()
        final_answer, node_relation = handler.qa_main(question)
        if len(final_answer) == 0:
            resData = {
                "resCode": 0,  # 非0即错误 1
                "data": [],  # 数据位置，一般为数组
                "message": '数据为空'
            }
            return jsonify(resData)

        resData = {
            "resCode": 0,  # 非0即错误 1
            "data": final_answer[0],  # 数据位置，一般为数组
            "message": '搜索结果'
        }
        return jsonify(resData)
    else:
        resData = {
            "resCode": 1, # 非0即错误 1
            "data": [],# 数据位置，一般为数组
            "message": '请求方法错误'
        }
        return jsonify(resData)



if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=1943, debug=True)
    app.run()

from flask import Flask, render_template, jsonify, request
import json
import re
import rsa
import base64
import time
import random
from QAmain import KGQA
from NewsCenter import News
from DataCenter import GetData
from SelfCheck import judge
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
    sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", str)
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


@app.route('/index',methods=['POST', 'GET'])
def covid_data():
    if request.method == 'GET':
        cov_data = GetData()
        data = cov_data.get_china_data()
        resData = {
            "resCode": 0,  # 非0即错误 1
            "data": data,  # 数据位置，一般为数组
            "message": '新闻结果'
        }
        print(jsonify(resData))
        return jsonify(resData)


@app.route("/submit", methods=["GET", "POST"])
def submit():  # 获取自检数据及提交
    # 由于POST、GET获取数据的方式不同，需要使用if语句进行判断
    if request.method == "POST":
        self_test = request.form.get("self_test",type=str)  # 一个数组？
    if request.method == "GET":
        self_test = request.form.get("self_test",type=str)
    print(self_test)
    print(str(self_test))
    self_test = str(self_test).strip().split(',')
    print(self_test)
    self_test = [ int(i) for i in self_test]

    result1 = judge(self_test)  # 根据结果显示相应内容
    return {'message': "success!", 'result1': result1}



@app.route('/search', methods=['POST', 'GET'])
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
        final_answer, node_relation = handler.qa_main(key)
        if len(final_answer) == 0:
            resData = {
                "resCode": 0,  # 非0即错误 1
                "data": [],  # 数据位置，一般为数组
                "message": '数据为空'
            }
            return jsonify(resData)

        resData = {
            "resCode": 0,  # 非0即错误 1
            "data": [final_answer[0], node_relation[0]],  # 数据位置，一般为数组
            "message": '搜索结果'
        }
        print("结果")
        print([final_answer[0], node_relation[0]])
        return jsonify(resData)
    else:
        resData = {
            "resCode": 1,  # 非0即错误 1
            "data": [],  # 数据位置，一般为数组
            "message": '请求方法错误'
        }
        return jsonify(resData)


@app.route('/news', methods=['POST', 'GET'])
def news_view():
    if request.method == 'GET':
        new = News()
        n = 3
        news_data = new.get_news_limit(n)
        resData = {
            "resCode": 0,  # 非0即错误 1
            "data": news_data,  # 数据位置，一般为数组
            "message": '新闻结果'
        }
        print(jsonify(resData))
        return jsonify(resData)
    else:
        resData = {
            "resCode": 1,  # 非0即错误 1
            "data": [],  # 数据位置，一般为数组
            "message": '请求方法错误'
        }
        return jsonify(resData)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1943, debug=True)
    # app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run()

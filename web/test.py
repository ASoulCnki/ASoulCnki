# -*- coding: UTF-8 –*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/v1/api/check", methods=["GET", "POST"])
def test():
    time.sleep(3)
    data = {
        "code": 0,
        "message": "",
        "data": {
            "rate":
            0.1145141919780,
            "start_time":
            1624237336,
            "end_time":
            1624238336,
            "related": [{
                "text": "然然带我走吧",
                "author": "嘉然今天吃什么",
                "rate": "0.1145141919780"
            }, {
                "text": "拉姐,带我走吧😭😭",
                "author": "蒙古上单",
                "rate": "0.10667"
            }, {
                "text": "然然带我走吧",
                "author": "嘉然今天吃什么",
                "rate": "0.1145141919780"
            }, {
                "text": "拉姐,带我走吧😭😭",
                "author": "蒙古上单",
                "rate": "0.10667"
            }, {
                "text": "然然带我走吧",
                "author": "嘉然今天吃什么",
                "rate": "0.1145141919780"
            }, {
                "text": "拉姐,带我走吧😭😭",
                "author": "蒙古上单",
                "rate": "0.10667"
            }]
        }
    }
    return jsonify(data)


app.run(host="0.0.0.0", port=8000)

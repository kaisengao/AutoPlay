import Constant
import requests
import json


# 将文本内容发送给 图灵机器人SDK
def requestRobot(text):
    print("内容 = " + text)
    url = "http://openapi.tuling123.com/openapi/api/v2"
    data = {'reqType': 0, 'perception': {'inputText': {'text': text}},
            'userInfo': {'apiKey': Constant.ROBOT_KEY, 'userId': 'demo'}}
    # Post 请求提交  JSON提交
    result = requests.post(url=url, data=json.dumps(data).encode())
    print("机器人 = " + result.text)
    # 解析机器人的内容
    data = json.loads(result.text)['results'][0]['values']['text']
    # 返回机器人的内容
    return data

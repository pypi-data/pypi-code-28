import requests
import json
import base64
import os
import math
import sys
import operator
import ybc_config


__PREFIX = ybc_config.config['prefix']
__CHECK_URL = __PREFIX + ybc_config.uri + '/food'


def check(filename=''):
    """
    功能：识别一个图片是否为美食图片。

    参数 filename 是当前目录下期望被识别的图片名字，

    返回：是否为美食。
    """
    if not filename:
        return False

    url = __CHECK_URL
    filepath = os.path.abspath(filename)
    files = {
        'file': open(filepath, 'rb')
    }
    for i in range(3):
        r = requests.post(url, files=files)
        if r.status_code == 200:
            res = r.json()
            res['data']['confidence'] = str(math.ceil(res['data']['confidence']*100)) + '%'
            return res['data']['food']
        elif i < 2:
            continue
        else:
            raise ConnectionError('判别美食图片失败', r._content)


def _get_access_token():
    url = 'https://www.yuanfudao.com/tutor-ybc-course-api/aniToken.php'
    r = requests.post(url)
    res = r.json()
    return res['access_token']


def food(filename='', topNum=3):
    """
    功能：美食识别。

    参数 filename 是当前目录下期望被识别的图片名字，

    可选参数 topNum 是识别结果的数量，默认为 3 ，

    返回：图片的美食信息。
    """
    if not filename:
        return -1
    url = 'https://www.yuanfudao.com/tutor-ybc-course-api/imgFood.php'
    filepath = os.path.abspath(filename)
    b64img= base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
    data = {}
    data['b64img'] = b64img
    data['access_token'] = _get_access_token()
    data['topNum'] = topNum
    r = requests.post(url, data=data)
    res = r.json()
    if res['result'] :
        if topNum == 1:
            return res['result'][0]
        else:
            return res['result']

def food_name(filename='', topNum=3):
    """
    功能：美食名字识别。

    参数 filename 是当前目录下期望被识别的图片名字，

    可选参数 topNum 是识别结果的数量，默认为 3 ，

    返回：美食的名字。
    """
    if not filename:
        return -1
    url = 'https://www.yuanfudao.com/tutor-ybc-course-api/imgFood.php'
    filepath = os.path.abspath(filename)
    b64img= base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
    data = {}
    data['b64img'] = b64img
    data['access_token'] = _get_access_token()
    data['topNum'] = topNum
    r = requests.post(url, data=data)
    res = r.json()
    if res['result']:
        sorted_val = sorted(res['result'],key=operator.itemgetter('probability'),reverse=True)
        return sorted_val[0]['name']
    else:
        return '不知道是啥(＾Ｕ＾)ノ~ＹＯ'




def main():
    # res = food('test.jpg')
    # print(res)
    # print(check("test.jpg"))
    pass

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
# @Author : Aiden
# @Email : aidenlen@163.com
# @Time : 2020-6-1

import logging
import multiprocessing
import os
import random
import time
from os import makedirs
from os.path import exists

import requests

# 定义一些基础的变量
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s'
)
# 列表页的url
BASE_URL = 'https://gate.lagou.com/'
API_URL = 'https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessonDetail?lessonId={lessonid}' # 获取数据的接口

# 保存路径
# 保存的文件名
RESULTS_DIR = '52讲收集'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

# 保存路径
FILEPATH = r'D:\\Python\\目标网站\\[16]拉勾网课程爬取\\lagou_spider\\cqc52讲\\'

# 指定目录下的所有文件名, 放在这个列表
FILE_LIST = []


# 构造请求头
HEADER = {
    #'authorization': '$$$EDU_eyJraWQiOiJkMzEyNmVmMi04OGU4LTRkYTktODQ5YS1mMjk0OTRlMTU0ZTIiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ0Z3QiOiJfQ0FTX1RHVF9UR1QtN2E0ZGMwNmIxNWYyNDlmMGE5OTZiMTNiM2FlMzQxN2YtMjAyMTA1MzAyMjQ3MjQtX0NBU19UR1RfIiwic3ViIjoiMTI4MTQ2NzEiLCJpcCI6IjExMi45NC4xMDAuMTA2IiwiaXNzIjoiZWR1LmxhZ291LmNvbSIsInRva2VuVHlwZSI6MSwiZXhwIjoxNjIyOTkwODQ0LCJpYXQiOjE2MjIzODYwNDR9.AXT1uUZ6mCAtCckmf9Fo2GnFIM6cqMbGUFX0wgl4_UTPKqSezFJ8JxdKLa4APAFRTNANLl6UycQKB4VXhCR0aK-R_YGPfMhjTs1eECABtRgctTenaMOXhqfjcJ2Yd0GVwVq5PpOUOn4pe5Nllwv6nH8Rg7wI6_JeUMNIpO76sWfKrsii4pAmm7C9O8mUW5wqVezPv4fWXKuPYVDlXvFqxQpAs6JM7qC8jHFbq2R6kwyq9h_0b1WYR05EtLtZkLqNPNoza8_gC_Nj4i2yNtxTzlB6rrXDU42UBRqHNEZkXaPzy2N6r6d_mxzmHsfSfPpQJIDNhBRYaEziH2bRsvH6Lw',
    #'cookie': 'user-finger=e27885cf3555313ec15c57bcbdd06576; smidV2=20210530224620c1fa1e1a0e6861332e05d66d0c4c1df4000d2f84c8306d810; thirdDeviceIdInfo=%5B%7B%22channel%22%3A1%2C%22thirdDeviceId%22%3A%22WHJMrwNw1k/F+oJwiU6Uh3/lkvVVbCeUPXWIKflOmQL2nSHughiPpg4DwfBS1Ta+Ai5HoCbPjV5jpf1kPQ7yLKB3skZHyfdgLdCW1tldyDzmQI99+chXEiotMKxULklYnYp5HxsF710xcYulduuw4jgCHPPxycwCneu8bpbMPuOTJc3aMEBGDbEut+P6r8d+Eafx5vzPvb3W5RtLdrPX5vCnovXXLjYfIC8roAzszmLvPkpQZRVubWSQO6SZ+Rp+2F10/rPYNoNw%3D1487582755342%22%7D%2C%7B%22channel%22%3A2%2C%22thirdDeviceId%22%3A%22140%23WoMoS0e/zzPXszo2+bsu4pN8s7aJ6j3G8GhEu93VPbL9HxF1FKEjp6jMxlTcjzmw4QYSlp1zz/UGRzAbXFzxIxkHOph/zzrb22U3lp1xzW+7V2EqlaOz2PD+V+fxnTD/OSvZrI7Zb6IpROlkZghF0MnTWmCWtqq0o+I1nwByrp7HyLUVHyDt7SCeGhmIKQ+ch91AzyRe5R6CydZcRyxnYlYje9VzsqGUs4i8LP4CZw/FwzIVhCtE2DCEH1wrXBobPSjgudKZboRGDOyggdxOVAxHvQZh8PEUYwM6i6iwBZ3sHH1D8F863fzawhZhsekGTnKUrOlw4O8rOUO2zMxRAj+3yLm2ZKvKICU8rxAh3tvSW9hU7LLrph4QhtXD18fGfHNaW3vI9Jgkv4osxcvIoX3pn2MM1e+nLM1fed5wgL763/UIrp5HxgriCUr4UFgyZTiRwtIHnepGXO/o3jyOmX1xTJDoM/bGWe4r9XABZ9wblOu7dD0ITqmPSUSskpcHFXAZubkgHi/RY/bQAowvuygKcbTSaEJgy1CaroIugG0on2f+d+IAmGRWWWV4zrrdfbZPo0dhkBVwIp6GqZ3A3ySXTzP9vUOkUO241PQMywdeCcNhWgjNAmoHxuEUb7QvMnYckiJlQZP1KHFKKhRy8ij3GNy6AEmxAP/7CXYDd+6AqgRwqQV4dm8DC2G7VYzH5ubXigXb0a5duGz5gS4rRrNFEMuKIh3Vod3US3gIZg37M12YPQTipruMF2baT+yiyh0X6mTPhOIxmZZcDSViS+GjtDpbOK3O/AmHVTzaxYPjAmCEfifVlg6tfOnw8+OuvR5dKKhwlv+9/V074/IJm8YKPQmKPaP04zNgaKBgLm7Q37PHMHhkqm2kOt54DqgLYKhAs70L0LDYVIJwvMZWrQ/YPqPjM9kSzYutUsi4fSj7+ESXB1a44tkejVl7EQ+wyLx163BIRNPlPdXj1MHi%2CT2gAfLPamkGpiTps58_GhLl4sdSOUvSM33luIL6ogaXu8WGgr3-CIGcaHKqD_qqf8t4%3D%22%7D%5D; gate_login_token=076bdf878eed7e133ab28740e189f7dc89e1f522a6c6e4e6828c195ee711929b; LG_LOGIN_USER_ID=9263c7e3e23e481f5483b3c7df0a3b773192031c0b9a6c194bc395fbaaf2b84e; LG_HAS_LOGIN=1; edu_gate_login_token=$$$EDU_eyJraWQiOiJkMzEyNmVmMi04OGU4LTRkYTktODQ5YS1mMjk0OTRlMTU0ZTIiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ0Z3QiOiJfQ0FTX1RHVF9UR1QtN2E0ZGMwNmIxNWYyNDlmMGE5OTZiMTNiM2FlMzQxN2YtMjAyMTA1MzAyMjQ3MjQtX0NBU19UR1RfIiwic3ViIjoiMTI4MTQ2NzEiLCJpcCI6IjExMi45NC4xMDAuMTA2IiwiaXNzIjoiZWR1LmxhZ291LmNvbSIsInRva2VuVHlwZSI6MSwiZXhwIjoxNjIyOTkwODQ0LCJpYXQiOjE2MjIzODYwNDR9.AXT1uUZ6mCAtCckmf9Fo2GnFIM6cqMbGUFX0wgl4_UTPKqSezFJ8JxdKLa4APAFRTNANLl6UycQKB4VXhCR0aK-R_YGPfMhjTs1eECABtRgctTenaMOXhqfjcJ2Yd0GVwVq5PpOUOn4pe5Nllwv6nH8Rg7wI6_JeUMNIpO76sWfKrsii4pAmm7C9O8mUW5wqVezPv4fWXKuPYVDlXvFqxQpAs6JM7qC8jHFbq2R6kwyq9h_0b1WYR05EtLtZkLqNPNoza8_gC_Nj4i2yNtxTzlB6rrXDU42UBRqHNEZkXaPzy2N6r6d_mxzmHsfSfPpQJIDNhBRYaEziH2bRsvH6Lw; user_trace_token=20210530232101-308193db-3357-421c-9de5-dd529de141b8; privacyPolicyPopup=false; index_location_city=%E5%B9%BF%E5%B7%9E; LGUID=20210530232414-35aab52d-78f3-4e5a-897b-7dd53fe7bda0; _ga=GA1.2.732852910.1622388254; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1622388254; EDUJSESSIONID=ABAAABAAAECABEH6DEEBAF1BAF61995CE1AF769AC796AE4; kw_login_authToken="OyURcss+RMv9EESgQlDvSgD3i1Hu43meoXyW8tRDU0wrQH7J69WlOCp8JjvLYyct97FloTvsx8VibY9sCFjtzi+RXO75l7mWcsQo6LXbucG0f20tPl/HoNvgV37H/AUxMn5fVQREkh2B/IuKxryfg/tjskbrG27V8etX7Cz/qld4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; sensorsdata2015session=%7B%7D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2212814671%22%2C%22first_id%22%3A%22179bdbd751d16d-03d0792d9dc4e6-3e604809-2073600-179bdbd751e6ef%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2286.0.4240.198%22%7D%2C%22%24device_id%22%3A%22179bdbd751d16d-03d0792d9dc4e6-3e604809-2073600-179bdbd751e6ef%22%7D',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'x-l-req-header': '{"deviceType":1,"userToken":"$$$EDU_eyJraWQiOiJkMzEyNmVmMi04OGU4LTRkYTktODQ5YS1mMjk0OTRlMTU0ZTIiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ0Z3QiOiJfQ0FTX1RHVF9UR1QtN2E0ZGMwNmIxNWYyNDlmMGE5OTZiMTNiM2FlMzQxN2YtMjAyMTA1MzAyMjQ3MjQtX0NBU19UR1RfIiwic3ViIjoiMTI4MTQ2NzEiLCJpcCI6IjExMi45NC4xMDAuMTA2IiwiaXNzIjoiZWR1LmxhZ291LmNvbSIsInRva2VuVHlwZSI6MSwiZXhwIjoxNjIyOTkwODQ0LCJpYXQiOjE2MjIzODYwNDR9.AXT1uUZ6mCAtCckmf9Fo2GnFIM6cqMbGUFX0wgl4_UTPKqSezFJ8JxdKLa4APAFRTNANLl6UycQKB4VXhCR0aK-R_YGPfMhjTs1eECABtRgctTenaMOXhqfjcJ2Yd0GVwVq5PpOUOn4pe5Nllwv6nH8Rg7wI6_JeUMNIpO76sWfKrsii4pAmm7C9O8mUW5wqVezPv4fWXKuPYVDlXvFqxQpAs6JM7qC8jHFbq2R6kwyq9h_0b1WYR05EtLtZkLqNPNoza8_gC_Nj4i2yNtxTzlB6rrXDU42UBRqHNEZkXaPzy2N6r6d_mxzmHsfSfPpQJIDNhBRYaEziH2bRsvH6Lw"}'
}


def scrape(url):
    """通用get请求
    :parma 接口
    "return json格式
    """
    logging.info('正在爬取... {}'.format(url))
    try:
        response = requests.get(url, headers=HEADER)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error("爬取 {}, 获取到无效的状态代码: {} ".format(url, response.status_code))        
    except :
        logging.error("{} 爬取出错".format(url), exc_info=True)


def parse_json(dict_data):
    return {
        'title' : dict_data.get('theme'),
        'time' : dict_data.get('publishDate'),
        'textContent': dict_data.get('textContent')
    }
    
def save_repeat(filename):
    """查重函数"""
    for root, dirs, files in os.walk(FILEPATH):
        for file_single in files:
            FILE_LIST.append(file_single)
    if filename not in FILE_LIST:
        repeat = False # False 代表不重复
    else:
        repeat = True
    return repeat


def save_data(data, filename, repeat):
    repeat = save_repeat(filename)
    file = FILEPATH + filename
    text = data.get('textContent')
    if not repeat:
        # 加'b':表示要读写二进制数据
        with open(file, 'w', encoding='utf-8') as f:
            f.write(text)
        logging.info('{} 文件保存成功!'.format(filename))
    else:
        logging.info('{} 文件重复! 自动跳过下载'.format(filename))
     

def main(id):
    url = API_URL.format(lessonid=id)
    json_data = scrape(url)
    dict_data = json_data.get('content')
    data = parse_json(dict_data)
    filename = str(data.get('title')) + '.html'
    repeat = save_repeat(filename)
    save_data(data, filename, repeat)

            
if __name__ == '__main__':
    # 52讲一共是 lessonId 1661—1713，加上结束语lessonId 4506
    # main(4506)
    pool = multiprocessing.Pool(4)
    lessonids = range(1661, 1713 + 1) 
    pool.map(main, lessonids)
    pool.close()
    pool.join()


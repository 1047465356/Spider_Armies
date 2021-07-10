# -*- coding: utf-8 -*-
# @Author : Aiden
# @Email : aidenlen@163.com
# @Time : 2020-3-11

from fake_useragent import UserAgent
# 注意，py文件和json文件放在同级目录
ua = UserAgent(path='fake_useragent.json')
headers = {'User-Agent': ua.random}
print(headers)

"""
运行结果：
{'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36'}
"""
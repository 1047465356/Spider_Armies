# -*- coding: utf-8 -*-
# @Author : Aiden
# @Email : aidenlen@163.com
# @Time : 2020-3-11

from logging import exception
from os import write
import requests
from lxml import etree
import time
from fake_useragent import UserAgent

# 文件名
filename='proxy.txt'
# 代理容器
proxys_list = []
# 默认 True 开启代理检测（只生成可用proxy）
check = True
# 检测超时(秒)
timeout = 0.2
# 爬取总页数
total_page = 5

def scrape_url(page):
    time.sleep(1)
    print('\n===========正在爬取第{}页数据============'.format(page))
    url = 'https://www.kuaidaili.com/free/inha/{}'.format(page)
    headers = {'User-Agent': UserAgent(path='fake_useragent.json').random}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
    except Exception as e:
        print('Exception: {}, url: {}'.format(e, url))
    

def parse_html(response):
    tree = etree.HTML(response.text)
    trs = tree.xpath('//*[@id="list"]/table/tbody/tr')

    for tr in trs:
        ip_num = tr.xpath('./td[1]/text()')[0]
        ip_port = tr.xpath('./td[2]/text()')[0]
        ip_proxy = ip_num + ':' + ip_port
        if tr.xpath('./td[4]/text()')[0] == 'HTTP':
            proxy = {'http': 'http://' + ip_proxy}
        if tr.xpath('./td[4]/text()')[0] == 'HTTPS':
            proxy = {'https': 'https://' + ip_proxy}
        proxys_list.append(proxy)
    return proxys_list
        
def check_ip(proxys):
    print('\n===============开启检测================')
    checked_proxys = []
    for proxy in proxys:
        try:
            response = requests.get(url = 'https://www.baidu.com', proxies = proxy, timeout = timeout)
            if response.status_code == 200:
                checked_proxys.append(proxy)
        except Exception as e:
            print('Exception: {}, 检测不合格: {}'.format(e, proxy))
        else:
            print('检测合格: {}'.format(proxy))
    return checked_proxys

def save_ip(proxys):
    with open(filename, 'a', encoding='utf-8') as file:
        for proxy in proxys:
            file.write(str(proxy) + '\n')
    print('保存成功: ', filename)


if __name__ == '__main__':
    for page in range(1, total_page + 1):
        response = scrape_url(page)
        proxys = parse_html(response)
        #print(proxys)
    if check:
        checked_proxys = check_ip(proxys)
        save_ip(checked_proxys)
    else:
        save_ip(proxys)


    

    
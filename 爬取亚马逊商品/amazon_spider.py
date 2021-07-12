# -*- coding: utf-8 -*-
# @Author : Aiden
# @Email : aidenlen@163.com
# @Time : 2021-3-17
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions

# 定义搜索关键字
SEARCH_KEY = r"HDD"
# 目标网站
URL = r"https://www.amazon.com"
# 保存路径
SAVE_LOCAL = "amazon_{}_page{}.html"


class AmazonSpider(object):

    def __init__(self):
        self.option = ChromeOptions()
        # 无头模式
        self.option.add_argument('--headless')
        self.browser = webdriver.Chrome(options=self.option)
        # 隐藏webdriver属性
        self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })

    def scrape(self):
        """搜索框输入"""
        print("爬取url: ", URL, "关键字: ", SEARCH_KEY)
        self.browser.get(URL)
        self.browser.find_element_by_xpath('.//input[@id="twotabsearchtextbox"]').send_keys(SEARCH_KEY)
        self.browser.find_element_by_xpath('.//input[@id="nav-search-submit-button"]').click()
        self.browser.implicitly_wait(10)
        time.sleep(3)

    def save_data(self, filename):
        """保存文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(self.browser.page_source))

    def next_page(self):
        """获取下一页"""
        try:
            self.browser.find_element_by_xpath('.//ul[@class="a-pagination"]/li[@class="a-last"]').click()
            self.browser.implicitly_wait(10)
            time.sleep(3)
        except Exception as e:
            print(e, '没有发现下一页按钮, 爬取结束')
            return False
        return True

    def run(self):
        self.scrape()
        i = 1
        while True:
            print("关键字: {}, 正在爬取第 {} 页".format(SEARCH_KEY, i))
            filename = SAVE_LOCAL.format(SEARCH_KEY, i)
            self.save_data(filename)
            if not self.next_page():
                break
            i += 1
        self.browser.close()
        

if __name__ == '__main__':
    spider = AmazonSpider()
    spider.run()



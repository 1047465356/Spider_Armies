# -*- coding: utf-8 -*-
# @Author : Aiden
# @Email : aidenlen@163.com
# @Time : 2021-3-10
import asyncio
import csv
import aiohttp
import logging
from parsel import Selector
from aiohttp import ContentTypeError
from aiohttp import TCPConnector
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

class Spider(object):
    
    def __init__(self):
        # 并发量
        self.CONCURRENCY = 2
        self.semaphore = asyncio.Semaphore(self.CONCURRENCY )
        self.ua = UserAgent(path='fake_useragent.json')
        self.headers = {"User-Agent": self.ua.random}
        self.data = list()
        self.path = "weike_data.csv"
        self.keywords = [
            '采集', 
            '爬', 
            '数据',
        ]
        self.base_url = "https://task.epwk.com/page{page}.html?k={keyword}"
        self.total_page = 5
    
    async def scrape_api(self, url):
        async with self.semaphore:
            try:
                logging.info('正在爬取: %s', url)
                async with self.session.get(url) as response:
                    await asyncio.sleep(0.1)
                    return await response.text()
            except ContentTypeError as e:
                logging.error('爬取错误: %s', url, exc_info=True)
    
    async def scrape_index(self, url):
        text = await self.scrape_api(url)

        selector = Selector(text)
        content_lists = selector.xpath('//*[@id="__layout"]/div/div[4]/div[3]/div[1]/div[3]/div')
        divs = content_lists.xpath('.//div[@class="itemblock"]')
        # print(divs[0]) 
        for div in divs:
            detail = dict()
            title = div.xpath('.//a[@class="text_over"]/text()').get()
            right = div.xpath('.//div[@class="right"]/span/text()').getall()
            price = right[0]
            status = right[1]
            browser = div.xpath('.//div[@class="browser"]/div')
            modelName = browser[0].xpath('./text()').get()
            see = browser[1].xpath('./span/text()').get()
            bid = browser[2].xpath('./span/text()').get()
            time_left = browser.xpath('.//div[@class="prcDesc"]/span/text()').get()
            

            # print(title.strip())
            # print(price.strip('￥'))
            # print(modelName.strip())
            # print(see.strip(' 人'))
            # print(bid.strip(' 人'))
            # print(time_left)
            # print(status.strip())
 
            detail['title'] = title.strip()
            detail['price'] = price.strip('￥')
            detail['modelName'] = modelName.strip()
            detail['see'] = see.strip(' 人')
            detail['bid'] = bid.strip(' 人')
            detail['time_left'] = time_left
            detail['status'] = status.strip()

            self.data.append(detail)

    async def scrape_main(self):
        self.session = aiohttp.ClientSession(connector=TCPConnector(ssl=False))
        urls = []
        for keyword in self.keywords:
            for page in range(1, self.total_page + 1):
                urls.append(self.base_url.format(page=page, keyword=keyword))

        scrape_detail_tasks = [asyncio.ensure_future(self.scrape_index(url)) for url in urls]
        detail_datas = await asyncio.gather(*scrape_detail_tasks)

        logging.info('len(detail_datas): %s', len(detail_datas))
        logging.info(detail_datas)

        await self.session.close()
        
    def write_csv_file(self):
        head = ["项目标题", "项目价格", "招标类型", "已看人数", "投标人数", "剩余投标时间",
                "当前状态"]
        keys = ["title", "price", "modelName", "see", "bid",
                "time_left", "status"]

        try:
            with open(self.path, 'a', newline='', encoding='utf_8_sig') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                if head is not None:
                    writer.writerow(head)
                for item in self.data:
                    row_data = []
                    for k in keys:
                        row_data.append(item[k])
                    writer.writerow(row_data)
                logging.info("Write a CSV file to path %s Successful.", self.path)
        except Exception as e:
            logging.error("Exception: %s, Fail to write CSV to path: %s", self.path, e , exc_info=True)

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.scrape_main())
        self.write_csv_file()


if __name__ == '__main__':
    spider = Spider()
    spider.run()
    


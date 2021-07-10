# -*- coding: utf-8 -*-
# @Author : Aiden
# @Email : aidenlen@163.com
# @Time : 2021-3-17
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
        self.path = "yuanjisong_data.csv"
        self.base_url = "https://www.yuanjisong.com/job/allcity/page{page}"
        self.total_page = 10
    
    async def scrape_api(self, url):
        async with self.semaphore:
            try:
                logging.info('正在爬取: %s', url)
                async with self.session.get(url) as response:
                    await asyncio.sleep(1)
                    return await response.text()
            except ContentTypeError as e:
                logging.error('爬取错误: %s', url, exc_info=True)
    
    async def scrape_index(self, url):
        text = await self.scrape_api(url)
        
        selector = Selector(text)
        weui_panels = selector.css('.weui_panel')
        for weui_panel in weui_panels:
            detail = dict()
            title = weui_panel.xpath('.//div[@class="topic_title"]/text()').get()
            price = weui_panel.xpath('.//span[@class="rixin-text-jobs"]/text()').get()
            desc = weui_panel.xpath('.//p[@class="media_desc_adapt "]/text()').get()
            work_time = weui_panel.xpath('.//p[@class="media_desc_adapt"]/span[3]/text()').get()
            bid = weui_panel.xpath('.//i[@class="i_post_num"]/text()').get()
        
            # print(title.strip())
            # print(price)
            # print(desc.strip())
            # print(work_time)
            # print(bid)
            # break

            detail['title'] = title.strip()
            detail['price'] = price
            detail['desc'] = desc.strip()
            detail['work_time'] = work_time
            detail['bid'] = bid

            self.data.append(detail)

    async def scrape_main(self):
        self.session = aiohttp.ClientSession(connector=TCPConnector(ssl=False))
        urls = []
        for page in range(1, self.total_page + 1):
            urls.append(self.base_url.format(page=page))

        scrape_detail_tasks = [asyncio.ensure_future(self.scrape_index(url)) for url in urls]
        detail_datas = await asyncio.gather(*scrape_detail_tasks)

        logging.info('len(detail_datas): %s', len(detail_datas))
        logging.info(detail_datas)

        await self.session.close()
        
    def write_csv_file(self):
        head = ["项目标题", "总价", "描述", "工时", "投标人数"]
        keys = ["title", "price", "desc", "work_time", "bid"]

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
            logging.e("Exception: %s, Fail to write CSV to path: %s", self.path, e, exc_info=True)

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.scrape_main())
        self.write_csv_file()


if __name__ == '__main__':
    spider = Spider()
    spider.run()
    


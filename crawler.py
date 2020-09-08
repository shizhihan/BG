import scrapy

from app import db
from models import Result

class MySpider(scrapy.Spider):
    name = 'myspider'
    id = None

    def __init__(self, *args, **kwargs):
        self.task_id = kwargs.pop('task_id', 0)
        self.keyword = kwargs.pop('keyword', '')

        url = kwargs.pop('url', '')
        if not url:
            raise Exception('Need url parameter')
        self.start_urls = [url]
        self.logger.info(self.start_urls)
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        for link in response.xpath('//a'):
            title = link.xpath('./text()').get()
            href = link.xpath('./@href').get()

            if not title or not href:
                continue

            if title.find(self.keyword) != -1:
                result = Result(task_id=self.task_id, title=title, href=href)
                db.session.add(result)
                db.session.commit()
                yield result

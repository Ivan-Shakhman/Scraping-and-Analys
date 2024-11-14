from pathlib import Path
import scrapy

class SneakySpider(scrapy.Spider):
    name = 'sneaky'

    def start_requests(self):
        urls = [
            "https://www.work.ua/jobs-python/?page=1",
            "https://www.work.ua/jobs-python/?page=2",
            "https://www.work.ua/jobs-python/?page=3"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"sneaky_{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved {filename}")
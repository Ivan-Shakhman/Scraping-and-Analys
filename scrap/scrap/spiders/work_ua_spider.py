from pathlib import Path
import scrapy

import scrap.items
from scrap import items


class JobSpider(scrapy.Spider):
    name = "job_spider"

    def start_requests(self):
        urls = [
            "https://www.work.ua/jobs-python/?page=1",
            "https://www.work.ua/jobs-python/?page=2",
            "https://www.work.ua/jobs-python/?page=3"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jobs = response.css("div.mb-lg h2 a::attr(href)").getall()
        for job in jobs:
            yield response.follow(job, callback=self.parse_job)

    def parse_job(self, response):
        item = items.ScrapItem()
        item["title"] = response.css("h1.my-0::text").get()
        item["company"] = response.css(".li.text-indent a.inline span.strong-500::text").get()
        print("-" * 100)
        print(item["title"])
        print("-" * 100)
        yield item
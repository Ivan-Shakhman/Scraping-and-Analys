import scrapy
from scrap.items import ScrapItem  # Предполагается, что ScrapItem настроен корректно

class JobSpider(scrapy.Spider):
    name = "job_spider"
    start_urls = [
        "https://www.work.ua/jobs-python/?page=1",
        "https://www.work.ua/jobs-python/?page=2",
        "https://www.work.ua/jobs-python/?page=3"
    ]

    def parse(self, response):
        jobs = response.css("div.mb-lg h2 a::attr(href)").getall()
        for job in jobs:
            yield response.follow(job, self.parse_job)

    def parse_job(self, response):
        item = ScrapItem()
        item["title"] = response.css("h1.my-0::text").get().strip()  # Удаляем лишние пробелы
        item["company"] = response.css("li.text-indent a.inline span::text").get().strip()
        item["location"] = response.css("li.text-indent::text").re_first(r"\s*(\S.*\S)\s*$").strip()
        item["skills"] = [skill.strip() for skill in response.css("li.no-style span.ellipsis::text").getall()]

        yield item

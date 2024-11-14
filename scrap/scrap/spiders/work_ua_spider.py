import time
from os import times
import re
import scrapy
from scrap.items import ScrapItem


def find_year(required_experience: str) -> int:
    match = re.search(r"\d+", required_experience)
    return int(match.group())


class JobSpider(scrapy.Spider):
    name = "job_spider"
    start_urls = ["https://www.work.ua/jobs-python/?page=1"]

    def parse(self, response):
        jobs = response.css("div.mb-lg h2 a::attr(href)").getall()
        for job in jobs:
            yield response.follow(job, self.parse_job)

        next_page = response.css("li.circle-style.add-left-sm a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_job(self, response):
        item = ScrapItem()
        item["title"] = response.css("h1.my-0::text").get().strip()
        item["company"] = (
            response.css("li.text-indent a.inline span::text").get().strip()
        )
        item["location"] = (
            response.css("li.text-indent::text").re_first(r"\s*(\S.*\S)\s*$").strip()
        )
        item["skills"] = [
            skill.strip()
            for skill in response.css("li.no-style span.ellipsis::text").getall()
        ]
        additional = (
            response.xpath(
                "//li[contains(@class, 'text-indent')]//span[contains(@class, 'glyphicon-tick')]/following-sibling::text()"
            )
            .get()
            .strip()
        )
        additional = additional.split(".")
        for add in additional:
            print("-" * 100)
            print(add)
            print("-" * 100)
            if "Досвід" in add:
                item["experience_required"] = find_year(add)
                additional.remove(add)
                break
        item["additional_info"] = additional

        yield item

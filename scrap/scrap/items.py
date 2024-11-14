# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    place = scrapy.Field()
    skills = scrapy.Field()

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RocketdataItem(scrapy.Item):
    # define the fields for your item here like:
    owner_name = scrapy.Field()
    owner_link = scrapy.Field()
    link_rep = scrapy.Field()
    name_rep = scrapy.Field()
    about = scrapy.Field()
    link_site = scrapy.Field()
    stars = scrapy.Field()
    watching = scrapy.Field()
    forks = scrapy.Field()
    commit_count = scrapy.Field()
    commit_author = scrapy.Field()
    commit_name = scrapy.Field()
    commit_datetime = scrapy.Field()
    release_count = scrapy.Field()
    release_version = scrapy.Field()
    release_datetime = scrapy.Field()

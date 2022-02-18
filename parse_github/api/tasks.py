from parse_github.celery import app
from scrapy.crawler import CrawlerProcess
from rocketdata.rocketdata.spiders.git_spider import GitSpider
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from rocketdata.rocketdata import spiders
import rocketdata.rocketdata


@app.task
def initial_scraper(name_rep):
    crawler_settings = Settings()
    crawler_settings.setmodule(module=rocketdata.rocketdata)
    # process = CrawlerProcess(settings=crawler_settings)
    process = CrawlerProcess({'BOT_NAME': 'rocketdata',
                              'SPIDER_MODULES': ['rocketdata.rocketdata.spiders'],
                              'NEWSPIDER_MODULE': 'rocketdata.rocketdata.spiders',
                              'ROBOTSTXT_OBEY': False,
                              'DOWNLOAD_DELAY': 0.20,
                              'LOG_FILE': 'scrapy.log',
                              'LOG_LEVEL': 'DEBUG',
                              'ITEM_PIPELINES': {
                                  'rocketdata.rocketdata.pipelines.RocketdataPipeline': 300,

                              }
                              })
    GitSpider.name_git = name_rep
    process.crawl(GitSpider)
    process.start()

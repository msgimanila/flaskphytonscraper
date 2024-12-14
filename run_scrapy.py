from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_spider():
    # Load Scrapy project settings
    process = CrawlerProcess(get_project_settings())

    # Specify the spider to run
    process.crawl("my_spider")  # Replace with your spider's name

    # Start the crawling process
    process.start()
 
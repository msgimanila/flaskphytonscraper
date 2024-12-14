import scrapy

class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["https://www.wired.com/tag/blogs/"]
    start_urls = ["https://www.wired.com/tag/blogs/"]

    def parse(self, response):
        # Extract the page title
        title = response.xpath('//title/text()').get()
        print(f"Page Title: {title}")

        # Extract all links on the page
        links = response.xpath('//a/@href').getall()

        # Store the results
        yield {
            'title': title,
            'links': links
        }

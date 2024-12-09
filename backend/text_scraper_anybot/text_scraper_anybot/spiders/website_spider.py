import scrapy

class WebsiteSpiderSpider(scrapy.Spider):
    name = "website_spider"
    allowed_domains = ["responseinfoinc.com"]  # Replace with your target domain
    start_urls = ["https://responseinfoinc.com/"]  # Replace with the start URL

    def parse(self, response):
        # Extract text content from the page
        text = response.xpath("//body//text()").getall()
        cleaned_text = " ".join(
            [line.strip() for line in text if line.strip() and "jquery" not in line.lower() and "$" not in line]
        )

        # Save as JSON
        yield {
            "url": response.url,
            "text": cleaned_text,
        }

        # Follow links to other pages
        for href in response.xpath("//a/@href").getall():
            yield response.follow(href, self.parse)
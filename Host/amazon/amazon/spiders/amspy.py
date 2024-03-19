import scrapy
from ..items import AmazonItem

class AmspySpider(scrapy.Spider):
	name = "amspy"
	allowed_domains = ["amazon.in"]
	start_urls = ["https://amazon.in"]

	custom_settings = {
    'FEEDS': {
        'data.csv': {'format': 'csv', 'overwrite': True},
    }, 
    'USER_AGENTS': [
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59',
    ],
}


	def __init__(self,slink):
		self.slink=slink

	def start_requests(self):
		# search=input('enter: ')
		search = self.slink
		if len(search)>0:
			yield scrapy.Request(
			url=search,
			callback=self.parse_amazon,
			)

	def parse_amazon(self, response):
		data = response.xpath('//div[@id="cm-cr-dp-review-list"]//div[@data-hook="review-collapsed"]/span')
		for feed in data:
			li = feed.get()
			li = li.replace("<span>", " ").replace("</span>", " ").replace("<br>", " ")
			item = AmazonItem()
			item['text'] = li
			yield item


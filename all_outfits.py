import json
import scrapy

class shopLookOutfit(scrapy.Spider):
    name = 'shoplook_outfit'

    shoplook_base_url = 'https://shoplook.io/api/outfits/feed/?page=%s&page_size=200'

    download_delay = 1.5

    json_headers =  {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
        'Accept': 'application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    }

    def start_requests(self):
        yield scrapy.http.Request(self.shoplook_base_url % 1, headers=self.json_headers)

    def parse(self,response):
        data = json.loads(response.body)
        for item in data.get('results', []):
            yield item

        if data['next']:
            yield scrapy.Request(data['next'], callback=self.parse, headers=self.json_headers)


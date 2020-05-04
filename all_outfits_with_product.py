import json
import scrapy
import re

#base_url = "https://shoplook.io/api/outfits/%s/products/"
#
#with open("all_outfits.json", 'r') as f:
#    outfits = json.load(f)
#
#count=0
#for outfit in outfits:
#    print(base_url % outfit['id'])
#    count+=1
#    if count>10:
#        break

class shopLookOutfit(scrapy.Spider):
    name = 'shoplook_outfit_products'

    # delay working
    download_delay = 1.5

    json_headers =  {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
        'Accept': 'application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    }

    def start_requests(self):
        base_url = "https://shoplook.io/api/outfits/%s/products/"

        #### CHANGE HERE!
        # with open("all_outfits.json", 'r') as f:
        # with open("all_outfits_small.json", 'r') as f:
        # with open("all_outfits_head_30k.json", 'r') as f:
        with open("all_outfits_30k_35k.json", 'r') as f:
            outfits = json.load(f)

        for outfit in outfits:
            yield scrapy.http.Request(base_url % outfit['id'], headers=self.json_headers)

    def parse(self,response):
        try:
            outfit_id = re.search('outfits/(.+?)/products', response.request.url).group(1)
        except AttributeError:
            outfit_id = '' # apply your error handling
        data = json.loads(response.body)
        outfit_data = data['results']
        yield { "outfit_id": outfit_id,
                "products": outfit_data }

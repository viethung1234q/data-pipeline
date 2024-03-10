import json
import os
from datetime import datetime

import scrapy
from scrapy.crawler import CrawlerProcess

DIR = os.path.join(os.path.abspath(__file__ + "/../../"), "output", "luigi_article.jsonl")

class LuigiSubprocessSpider(scrapy.Spider):
    name = "luigisub"
    start_urls = [
        'https://vietnamnet.vn/ngu-ngon-thoi-nhe-xon-xang-2034444.html'
    ]

    def parse(self, response):
        print("\n\nCrawling from: " + response.url)
        
        """
        Crawled data
        """
        article_id = response.css('[articleid]::attr(articleid)').get()
        title = response.css('div.newsFeatureBox > div.newsFeature__header > h1::text').get()
        description = response.css('div.newFeature__main-textBold::text').get()

        # Extract date: DD/MM/YYYY and convert to SQL DATE format
        date = response.css('div.breadcrumb-box__time span::text').get() 
        splitDate = date.strip().split(' ')
        date_obj = datetime.strptime(splitDate[0], "%d/%m/%Y") # convert to date object
        normDate = date_obj.strftime('%Y-%m-%d') # convert to SQL DATE format

        category = response.css('div.breadcrumb-box__link a::text').get()
        author = response.css('p.newsFeature__author-info a::text').get()
        
        tag = response.css('div.list-tag-related li[class=""] a::text').getall()
        tag = [i.strip() for i in tag]

        data = {
            'article_id': article_id.strip(),
            'title': title.strip(),
            'description': description.strip(),
            'date': normDate,
            'category': category.strip(),
            'link': response.url,
            'author': author.strip(),
            'tag': tag,
            'update_date': datetime.now().strftime('%Y-%m-%d') # convert to SQL DATE format
        }

        # Write crawled data to file
        data_json_object = json.dumps(data, ensure_ascii=False)
        with open(DIR, 'w', encoding="utf_8") as f:
            f.write(data_json_object)

process = CrawlerProcess()
process.crawl(LuigiSubprocessSpider)
process.start()

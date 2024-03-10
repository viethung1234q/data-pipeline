import json
import os
from datetime import datetime

import scrapy
from scrapy.crawler import CrawlerProcess

"""
Path to file contain crawled data
"""
now = datetime.now()
day_month_year = now.strftime('%d_%m_%Y') # DD_MM_YYYY
ROOT_DIR = os.path.abspath(__file__ + "/../../") # parent dir
output_dir_1 = os.path.join('mnt', ROOT_DIR)
output_dir_2 = os.path.join('output', f'{day_month_year}.jsonl')
OUTPUT_PATH = os.path.join(output_dir_1, output_dir_2)


class VnnetSpider(scrapy.Spider):
    name = "vnnet"
    allowed_domains = ["vietnamnet.vn"]
    start_urls = ['https://vietnamnet.vn']

    def parse(self, response):
        if response.status == 200 and response.css('meta[content="website"]').get() is None:
            print("\n\nCrawling from: " + response.url)
            
            """
            Crawled data
            """
            article_id = response.css('[articleid]::attr(articleid)').get()
            title = response.css('div.newsFeatureBox > div.newsFeature__header > h1::text').get()
            description = response.css('div.newFeature__main-textBold::text').get()

            # Extract date: DD/MM/YYYY and convert to SQL DATE format
            date = response.css('div.breadcrumb-box__time span::text').get() 
            split_date = date.strip().split(' ')
            date_obj = datetime.strptime(split_date[0], "%d/%m/%Y") # convert to date object
            norm_date = date_obj.strftime('%Y-%m-%d') # convert to SQL DATE format

            category = response.css('div.breadcrumb-box__link a::text').get()
            author = response.css('p.newsFeature__author-info a::text').get()
            
            tag = response.css('div.list-tag-related li[class=""] a::text').getall()
            tag = [i.strip() for i in tag]

            data = {
                'article_id': article_id.strip(),
                'title': title.strip(),
                'description': description.strip(),
                'date': norm_date,
                'category': category.strip(),
                'link': response.url,
                'author': author.strip(),
                'tag': tag,
                'update_date': datetime.now().strftime('%Y-%m-%d') # convert to SQL DATE format
            }

            # Write crawled data to file
            with open(OUTPUT_PATH, 'a', encoding="utf_8") as f:
                if data: 
                    data_json_object = json.dumps(data, ensure_ascii=False)
                    f.write(data_json_object)
                    f.write('\n')

        yield from response.follow_all(
            css = 'div div.feature-box__image a::attr(href), nav.header__nav > div > ul > li:not([class]) > a::attr(href)',
            callback = self.parse
        )

# Run Scrapy without using "scrapy crawl" command
process = CrawlerProcess()
process.crawl(VnnetSpider)
process.start()
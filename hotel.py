import os 
import logging
import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from datetime import datetime, timedelta


def get_url():
    checkin_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    checkout_date = (datetime.today() + timedelta(days=8)).strftime('%Y-%m-%d')

    df = pd.read_csv(r'C:\Users\Malika\Desktop\JEDHA\jedha_formation\fullstack\web_scraping\kayak_project\kayak_projetc_v2\ranking_by_weather_score_v2.csv')
    
    urls = []
    
    
    for index, row in df.iterrows():
        city_name = row['name'].replace(" ", "%20")
        url = f'https://www.booking.com/searchresults.fr.html?ss={city_name}&checkin={checkin_date}&checkout={checkout_date}&group_adults=2&no_rooms=1&group_children=0'
        urls.append(url)
        logging.info(f"URL generated: {url}") 

    return urls

class BookingSpider(scrapy.Spider):
    name = 'booking_spider'

    def start_requests(self):
        urls = get_url()

        for url in urls:
            logging.info(f"Visiting URL: {url}")
            yield scrapy.Request(url=url, callback=self.parse)
    
    
    def parse(self, response):
        hotels = response.css('div.f6431b446c.a15b38c233')
        for hotel in hotels[:20]:
            hotel_name = hotel.css('::text').get().strip()

            hotel_url = hotel.xpath('ancestor::a/@href').get()
            full_url = response.urljoin(hotel_url)

            yield {
                'hotel_name': hotel_name,
                'hotel_url': full_url
            }


filename = "hotel_url.json"
if filename in os.listdir('.'):  
    os.remove(filename)

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'LOG_LEVEL': logging.INFO,
        "FEEDS": {
            filename: {"format": "json"}
        },
    })

process.crawl(BookingSpider)
process.start()

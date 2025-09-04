import json
import scrapy
import os
from scrapy.crawler import CrawlerProcess


with open('hotel_url.json', 'r', encoding='utf-8') as file:
    hotels_data = json.load(file)


class HotelDescriptionSpider(scrapy.Spider):
    name = 'hotel_description_spider'

    def start_requests(self):
        
        for hotel in hotels_data:
            hotel_name = hotel.get('hotel_name')
            hotel_url = hotel.get('hotel_url')

            if hotel_url:
                yield scrapy.Request(url=hotel_url, callback=self.parse, meta={'hotel_name': hotel_name})

    def parse(self, response):
        
        hotel_name = response.meta['hotel_name']

        description = response.css('p.a53cbfa6de.b3efd73f69::text').getall()
        description_text = ' '.join(description).strip()

        address = response.css('#showMap2 > span.hp_address_subtitle.js-hp_address_subtitle.jq_tooltip::text').get()
        address = address.strip() if address else "Adresse non disponible"

        rating = response.css('#js--hp-gallery-scorecard > a > div > div > div > div.a3b8729ab1.d86cee9b25::text').get()
        rating = rating.strip() if rating else "Note non disponible"

        yield {
            'hotel_name': hotel_name,
            'description': description_text,
            'address': address,
            'rating': rating
        }

filename = "hotel_description_full.json"
if filename in os.listdir('.'):  
    os.remove(filename)

process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        "FEEDS": {
            filename: {"format": "json"}
        },
    })

process.crawl(HotelDescriptionSpider)
process.start()

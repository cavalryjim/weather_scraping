import scrapy
import csv
import os.path


class WeatherSpider(scrapy.Spider):
    name = "weather"

    start_urls = [
        'https://forecast.weather.gov/MapClick.php?lat=30.4434&lon=-91.1866', # Baton Rouge
        'https://forecast.weather.gov/MapClick.php?lat=29.9537&lon=-90.0777', # New Orleans
    ]

    def parse(self, response):
        file_name = 'outfile.csv'
        city = response.css("h2.panel-title::text").get()
        days = response.css("div.tombstone-container")

        if os.path.exists(file_name):
            out_file = open(file_name, 'a')
            csv_writer = csv.writer(out_file)
        else:
            out_file = open(file_name, 'w')
            csv_writer = csv.writer(out_file)
            csv_writer.writerow( [ 'city', 'period', 'short_desc', 'temp', 'desc' ])

        for day in days:
            period = day.css("p.period-name::text").get()
            short_desc = day.css("p.short-desc::text").get()
            temp = day.css("p.temp::text").get()
            desc = day.xpath("p/img/@alt").extract()[0]
            csv_writer.writerow( [ city, period, short_desc, temp, desc ] )

        out_file.close()

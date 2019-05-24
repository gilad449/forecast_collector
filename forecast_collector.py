#!/usr/bin/python3

import requests # the package is used for getting the website page
from bs4 import BeautifulSoup as bs # beautifulsoup is used in order to parse the page and its elements 
import json # convert dictionary into a Json formatted object

class forecastCollector():

    def __init__(self):
        self.url = "https://weather.com/weather/hourbyhour/l/ISXX0026:1:IS"

    def get_bs_page(self):
        """ takes url as input and returns a beautifulsoup object """
        
        try:
            page = requests.get(self.url)
            bs_page = bs(page.text)
            return bs_page
        except Exception as e:
            print(e) 

    def get_hourly_forecast(self):
        """ extracts information on hourly forecasts table using beautifulsoup and returns a Json """

        hourly_forecasts = {}
        bs_page = self.get_bs_page()
        times = bs_page.find_all("span",{"class":"dsx-date"})
        times = [time.text for time in times]
        descriptions = bs_page.find_all("td",{"headers":"description"})
        descriptions = [description.find("span").text for description in descriptions]
        temps = bs_page.find_all("td",{"headers":"temp"})
        temps = [temp.find("span").text.replace("°","") for temp in temps]
        feels = bs_page.find_all("td",{"headers":"feels"})
        feels = [feel.find("span").text.replace("°","") for feel in feels]
        precips = bs_page.find_all("td",{"headers":"precip"})
        precips = [precip.find_all("span")[1].text for precip in precips]
        humidity = bs_page.find_all("td",{"headers":"humidity"})
        humidity = [humid.find("span").text for humid in humidity]
        winds = bs_page.find_all("td",{"headers":"wind"})
        winds = [wind.find("span").text for wind in winds]
        
        for i in range(times.__len__()):
            hourly_forecasts[times[i]] = {"DESC":descriptions[i],"TEMP":temps[i],"FEEL":feels[i],"PRECIP":precips[i],"HUMIDITY":humidity[i],"WIND":winds[i]}

        with open("forecast_data.json","w") as file:
            json.dump(hourly_forecasts, file)
        
if __name__ == "__main__":

    fc = forecastCollector()
    fc.get_hourly_forecast()
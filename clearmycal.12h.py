#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python
# -*- coding: utf-8 -*-

# <bitbar.title>ClearMyCal</bitbar.title>
# <bitbar.version>v0.0.1</bitbar.version>
# <bitbar.author>Matt Arderne</bitbar.author>
# <bitbar.author.github>seripap</bitbar.author.github>
# <bitbar.desc>ClearMyCal xbar plugin.</bitbar.desc>
# <bitbar.image></bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>


import requests
import json
from random import randint
from datetime import datetime
import os
from statistics import mean

# CONFIG

# threshold that the temp must break in order to get an alert
PERCTEMP = 1.20

VCKEY=os.environ['visualcrossing']


def weather_scale(): 
	"""
	relative scale of the various weather descriptions
	more documents here
	https://www.visualcrossing.com/resources/documentation/weather-api/weather-condition-fields/"""
	return {
		    '1': 'clear-day',
		    '1': 'clear-night',
		    '2': 'partly-cloudy-day',
		    '2': 'partly-cloudy-night',
		    '3': 'wind',
		    '4': 'cloudy',
		    '5': 'fog',
		    '6': 'rain',
		    '7': 'sleet',
		    '8': 'snow'
					}

def get_historical():
	"""
	gets the historical data for the previous few weeks 
	and returns the average temp for that period
	"""

	try:
		wx = (requests.get(f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?aggregateHours=24&combinationMethod=aggregate&period=last30days&maxStations=-1&maxDistance=-1&contentType=json&unitGroup=metric&locationMode=single&key={VCKEY}&dataElements=default&locations=eynsham'))			
		wx = wx.json()

	except requests.HTTPError:
		return False
	
	try: 

		daily_data = {}

		maxtemp = 0
		counter = 0

		for item in wx['location']['values']:

			counter += 1
			maxtemp += item['maxt']
		
		average_maxtemp = maxtemp/counter

		return round(average_maxtemp,2)

	except requests.HTTPError:
		return requests.HTTPError

def get_forecast(average_maxtemp, delta):
	"""
	looks at the weather for the next week and compares it to the given average
	returns a dict of the dates and conditions that break the average
	delta is a variable indicating by how much the average must be broken in order to trigger alerg
	"""

	try:
		wx = (requests.get(f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?aggregateHours=24&combinationMethod=aggregate&contentType=json&unitGroup=metric&locationMode=single&key={VCKEY}&dataElements=default&locations=eynsham'))
		wx = wx.json()
	except requests.HTTPError:
		return False

	daily_data = {}

	counter = 0

	for item in wx['location']['values']:

		if int(item['maxt']) >= int(average_maxtemp*delta):
			

			daily_data[counter] = {}
			daily_data[counter]['maxt'] = item['maxt']
			daily_data[counter]['conditions'] = item['conditions']
			daily_data[counter]['date'] = datetime.fromtimestamp(item['datetime']/1000).strftime('%Y-%m-%d')

			counter += 1

		else:	
			return False

	
	return daily_data

		
def main():

	average = get_historical()
	forecast = get_forecast(average, PERCTEMP)

	if forecast:
		print('WX!')
		print('---')
		print('average: ' + str(average))
		for i in forecast.items():
			print(i[1]['date'] + ' temp: ' + str(i[1]['maxt']) + str(i[1]['conditions']))

if __name__ == "__main__":
	main()




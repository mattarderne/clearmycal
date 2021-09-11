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
import datetime
from datetime import datetime
import sqlite3
import os
from statistics import mean

import jsbeautifier
opts = jsbeautifier.default_options()
opts.indent_size = 2



conn = sqlite3.connect('/Users/mattarderne/Documents/notkak.db')
curr = conn.cursor()


def weather_scale(): 
		"""relative scale of the various weather descriptions
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

		try:
			wx = (requests.get('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?aggregateHours=24&combinationMethod=aggregate&period=last30days&maxStations=-1&maxDistance=-1&contentType=json&unitGroup=metric&locationMode=single&key=L69PGR8DVXWM7RZV3DQC4AVRW&dataElements=default&locations=eynsham'))
			wx = wx.json()
		except requests.HTTPError:
			return False

		# wx = wx['location']['values'][0]
		# print(jsbeautifier.beautify(json.dumps(wx), opts))

		daily_data = {}

		maxtemp = 0
		counter = 0

		for item in wx['location']['values']:

			counter += 1
			maxtemp += item['maxt']

			# datetime = item['datetime']
			# daily_data[datetime] = {}
			# daily_data[datetime]['temp'] = item['temp']
			# daily_data[datetime]['maxt'] = item['maxt']
			# daily_data[datetime]['visibility'] = item['visibility']
			# daily_data[datetime]['wspd'] = item['wspd']
			# daily_data[datetime]['datetimeStr'] = item['datetimeStr']
			# daily_data[datetime]['heatindex'] = item['heatindex']
			# daily_data[datetime]['cloudcover'] = item['cloudcover']
			# daily_data[datetime]['mint'] = item['mint']
			# daily_data[datetime]['datetime'] = item['datetime']
			# daily_data[datetime]['precip'] = item['precip']
			# daily_data[datetime]['weathertype'] = item['weathertype']
			# daily_data[datetime]['snowdepth'] = item['snowdepth']
			# daily_data[datetime]['humidity'] = item['humidity']
			# daily_data[datetime]['wgust'] = item['wgust']	
			# daily_data[datetime]['conditions'] = item['conditions']	
			# daily_data[datetime]['windchill'] = item['windchill']
			
		average_maxtemp = maxtemp/counter
		return round(average_maxtemp,2)

def get_forecast(average_maxtemp, delta):

		try:
			wx = (requests.get('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?aggregateHours=24&combinationMethod=aggregate&contentType=json&unitGroup=metric&locationMode=single&key=L69PGR8DVXWM7RZV3DQC4AVRW&dataElements=default&locations=eynsham'))
			wx = wx.json()
		except requests.HTTPError:
			return False

		# wx = wx['location']['values']
		# print(jsbeautifier.beautify(json.dumps(wx), opts))

		daily_data = {}

		for item in wx['location']['values']:
			print(average_maxtemp)
			print(delta*item['maxt'])
			break
			if int(average_maxtemp) > int(delta*item['maxt']):
				datetime = item['datetime']
				daily_data[datetime] = {}
				daily_data[datetime]['temp'] = item['temp']
				daily_data[datetime]['conditions'] = item['conditions']


				# daily_data[datetime]['maxt'] = item['maxt']
				# daily_data[datetime]['visibility'] = item['visibility']
				# daily_data[datetime]['wspd'] = item['wspd']
				# daily_data[datetime]['datetimeStr'] = item['datetimeStr']
				# daily_data[datetime]['heatindex'] = item['heatindex']
				# daily_data[datetime]['cloudcover'] = item['cloudcover']
				# daily_data[datetime]['pop'] = item['pop']
				# daily_data[datetime]['mint'] = item['mint']
				# daily_data[datetime]['datetime'] = item['datetime']
				# daily_data[datetime]['precip'] = item['precip']
		
				# daily_data[datetime]['snowdepth'] = item['snowdepth']
				# daily_data[datetime]['snow'] = item['snow']
				# daily_data[datetime]['humidity'] = item['humidity']
				# daily_data[datetime]['wgust'] = item['wgust']	
					
				# daily_data[datetime]['windchill'] = item['windchill']
			else:	
				return False

		
		return daily_data


class Compare():
	def __init__(self):
		self.something = 'foo'

	def past_compare_previous(self,past_week, coming_week):
		"""houses the logic to determine if the week coming is 
		much better than the determined previous period"""

		if (coming_week[0][2] > past_week[0][2]):
			return True;
		if (coming_week[1][2] > past_week[0][2]):
			return True;
		else:
			return False

	def warn(self, wx):
		"""The alert that gets printed on the xbar plugin if there is a good day coming""" 
		print('Alert')
		print('---')
		print(wx)


	def render_wx(self, wx):

		print('---')
		if daily_data[0]:
			for i in range(4):
				print(
							  str(daily_data[i]['timestamp'])
					+ '  ' + str(int(daily_data[i]['temperatureMin'])) +'-'+ str(int(daily_data[i]['temperatureMax'])) + ' C'
					)

		else:
			print('N/A')
		
def main():
	average = get_historical()
		
	print(get_forecast(average, 1.11))

	

if __name__ == "__main__":
	main()




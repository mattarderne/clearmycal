#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python
# -*- coding: utf-8 -*-

# <bitbar.title>Weather</bitbar.title>
# <bitbar.version>v3.5.0</bitbar.version>
# <bitbar.author>Matt Arderne</bitbar.author>
# <bitbar.author.github>seripap</bitbar.author.github>
# <bitbar.desc>Oxford Sailing Club xbar plugin.</bitbar.desc>
# <bitbar.image>https://cloud.githubusercontent.com/assets/683200/16276583/ff267f36-387c-11e6-9fd0-fc57b459e967.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>


import requests
import json
from random import randint
import datetime
from datetime import datetime
import sqlite3
import os



conn = sqlite3.connect('/Users/mattarderne/Documents/notkak.db')
curr = conn.cursor()


class Utils:

	@classmethod
	def weather_scale(self): 
		"""relative scale of the various weather descriptions"""
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

	@classmethod
	def calculate_bearing(self, bearing, compass_rose, additional=False):
		"""returns a windrose cardinal bearing, if additional Flag is set, it also returns the nearest two options"""
		if compass_rose == 16:
			dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
		if compass_rose == 8: 	
			dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
		if compass_rose == 4: 	
			dirs = ['^','<', 'v', '>']

		ix = round(bearing / (360. / len(dirs)))
		
		if additional:
			now = dirs[ix % len(dirs)],
			neg	 = 	dirs[ix-1 % len(dirs)]
			if ix >= compass_rose-1:
				# if the index needs something at the other end of the list
				pos	 = 	dirs[1 % len(dirs)]
			else:
				pos	 = 	dirs[ix+1 % len(dirs)]
			return now, neg, pos
		
		else:
			now = dirs[ix % len(dirs)]
			return now

	@classmethod
	def create_db(self):
		"""creates the db table, only necessary once"""

		sql = 	'''CREATE TABLE IF NOT EXISTS wx_history
			(   id CHAR(255) PRIMARY KEY NOT NULL, 
				dbtimestamp CHAR(255),
				timestamp CHAR(255),
				windSpeed REAL,
				windBearing REAL,
				windGust REAL,
				icon CHAR(255),
				temperatureMin REAL,
				temperatureMax REAL
			)
			'''
		# conn.execute('''ALTER TABLE wx_history ADD COLUMN date CHAR(255)''')
		conn.execute(sql)

	@classmethod				
	def load_db(self, entries):
		"""loads data into the database, line by line
			uses the hybrid primary key id
			which ensures that only one forecast record per future date gets added per day
			this is because forecasts change and so 
			there isn't much value in getting a new forecast with more frequency than daily
			"""

		for key in entries.items():

			meta_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			meta_date = datetime.now().strftime('%Y-%m-%d')
			
			id = meta_date+' '+str(key[1]['timestamp'])
			dbtimestamp = datetime.strptime(meta_timestamp, '%Y-%m-%d %H:%M:%S')
			timestamp = key[1]['timestamp']
			windSpeed = key[1]['windSpeed']
			windBearing = key[1]['windBearing']
			windGust = key[1]['windGust']
			icon = key[1]['icon']
			temperatureMin = key[1]['temperatureMin']
			temperatureMax = key[1]['temperatureMax']
			
			try:
				curr.execute("INSERT INTO wx_history (id,dbtimestamp,timestamp,windSpeed,windBearing,windGust,icon,temperatureMin,temperatureMax) VALUES (?,?,?,?,?, ?,?,?,?)", (id,dbtimestamp,timestamp,windSpeed,windBearing,windGust,icon,temperatureMin,temperatureMax))
				conn.commit()
			except:
				pass
		conn.commit()

	@classmethod	
	def get_forecasts(self, limit=8):
		"""queries the database, to get the latest versions of the future forecasts"""
		
		sql = """WITH latest_forecasts AS (
					SELECT
						DATE(timestamp, 'unixepoch', 'localtime') forecast_date,
						icon,
						temperatureMax,
						MAX(dbtimestamp)
					FROM
						wx_history
						GROUP BY 1
						
				)
				SELECT 
					"forecast_date",
					icon,
					temperatureMax
				FROM
					latest_forecasts
					WHERE "timestamp" > date('now')		
				"""
		rows = curr.execute(sql).fetchmany(int(limit))
		return rows

	@classmethod	
	def get_history(self, limit=14):
		"""queries the database, to history of the most likely actual weather for the past 2 weeks"""
		
		sql = """select 1	
				"""
		rows = curr.execute(sql).fetchmany(int(limit))
		return rows

class Forecast:
	def __init__(self):
		# get yours at https://darksky.net/dev
		self.api_key = os.environ['darksky']
		self.geo_api_key = ''
		# get yours API key for encode location at https://opencagedata.com
		self.manual_city = 'Eynsham'
		self.manual_latlng = '51.781605,-1.376999'

		# set to si for metric, leave blank for imperial
		self.units = 'si'

	def manual_location_lookup(self):
		if self.manual_latlng == "" or self.manual_city == "":
			return False;
		else:
			return { "loc": self.manual_latlng, "preformatted": self.manual_city }

	def get_wx(self):

		if self.api_key == "":
			return False

		location = self.manual_location_lookup() 

		if self.units == 'si':
			unit = 'C'
			distance = 'Knots'
			distance_short = 'km'
		else:
			unit = 'F'
			distance = 'mph'
			distance_short = 'mi'

		try:
			if 'loc' in location:
				wx = (requests.get('https://api.darksky.net/forecast/' + self.api_key + '/' + location['loc'] + '?units=' + self.units + "&v=" + str(randint(0,100))))
				wx = wx.json()
			else:
				return False
		except requests.HTTPError:
			return False


		daily_data = {}

		if 'daily' in wx:
			counter = 0
			for item in wx['daily']['data']:
				daily_data[counter] = {}
				daily_data[counter]['windSpeed'] = item['windSpeed']
				daily_data[counter]['windBearing'] = item['windBearing']
				daily_data[counter]['windGust'] = item['windGust']
				daily_data[counter]['timestamp'] = item['time']
				daily_data[counter]['icon'] = item['icon']
				daily_data[counter]['temperatureMin'] = item['temperatureMin']
				daily_data[counter]['temperatureMax'] = item['temperatureMax']
				daily_data[counter]['temperatureMinTime'] = item['temperatureMinTime']
				daily_data[counter]['temperatureMaxTime'] = item['temperatureMaxTime']
				daily_data[counter]['temperatureHigh'] = item['temperatureHigh']
				daily_data[counter]['temperatureHighTime'] = item['temperatureHighTime']
				daily_data[counter]['apparentTemperatureHigh'] = item['apparentTemperatureHigh']
				daily_data[counter]['apparentTemperatureHighTime'] = item['apparentTemperatureHighTime']

				counter += 1

		return daily_data

	def render_wx(self, wx):

		if self.api_key == '':
			print('Missing API key')
			print('---')
			print('Get an API Key | href=https://darksky.net/dev')
			return False

		daily_data = wx

		if daily_data is False:
			print('--')
			print('---')
			print('Could not get weather data at this time')
			return False

	###TOP BAR

		print('---')
		if daily_data[0]:
			for i in range(4):
				print(
							  str(daily_data[i]['timestamp'])
					+ '  ' + str(int(daily_data[i]['temperatureMin'])) +'-'+ str(int(daily_data[i]['temperatureMax'])) + ' C'
					)

		else:
			print('N/A')

class Compare():
	def __init__(self):
		self.something = 'foo'

	def compare(self,wx, past_week):
		if max(wx) > max(past_week):
			return True;
		else:
			return False

	def warn():
		if compare:
			print('Alert')
		else:
			return False
		
def main():
	
	### Get the latest forecast and load to db
	forecast = Forecast()
	wx = Forecast.get_wx(forecast)
	Forecast.render_wx(forecast, wx)
	Utils.create_db()
	Utils.load_db(wx)

	### compare the latest forecast to the recent week

	# pulls the "actual" data from the past n weeks
	past_week = Utils.get_history()

	# pulls the forecast for the next week
	print(past_week)

	conn.close()
	

main()




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


conn = sqlite3.connect('/Users/mattarderne/Documents/notkak.db')
curr = conn.cursor()


def weather_scale(): 
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

def create_db():
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
		conn.execute(sql)
			
def update_db(entries):
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
	
def query_forecasts(limit=8):
		"""queries the database, to get the latest versions of the future forecasts"""
		
		sql = """WITH latest_forecasts AS (
					SELECT
						DATE(timestamp,
							'unixepoch',
							'localtime') forecast_date,
						icon,
						temperatureMax,
						MAX(dbtimestamp)
					FROM
						wx_history
					GROUP BY
						1
				)
				SELECT
					forecast_date,
					icon,
					temperatureMax
				FROM
					latest_forecasts
				WHERE
					forecast_date > date('now')	
				"""
		rows = curr.execute(sql).fetchmany(int(limit))
		return rows

def query_history(limit=14):
		"""queries the database, 
		gets history of the most likely actual weather for the past 2 weeks
		Does this by taking the forecast from the day closest to the time the data was loaded
		This assumes that the next day forecast was close to what was actually experienced
		This could possibly be improved by pulling weather station data, but that might be inconsistent"""
		
		sql = """WITH historic_actuals AS (
					SELECT
						DATE(timestamp,
							'unixepoch',
							'localtime') historic_date,
							temperatureMax,
							icon,
						MAX(dbtimestamp)
					FROM
						wx_history
					GROUP BY
						1
				)
				SELECT
					historic_date,
					icon,
					temperatureMax
				FROM
					historic_actuals
				WHERE
					historic_date <= date('now')
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

		if self.api_key == '':
			print('Missing API key')
			print('---')
			print('Get an API Key | href=https://darksky.net/dev')
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
	
	### Get the latest forecast and load to db
	forecast = Forecast()
	wx = Forecast.get_wx(forecast)

	create_db()
	update_db(wx)

	### compare the latest forecast to the recent week

	# pulls the "actual" data from the past n weeks
	past_weeks = query_history()

	# pulls the forecast for the next week
	coming_week = query_forecasts() 

	compare = Compare()
	if compare.past_compare_previous(past_weeks, coming_week):
		compare.warn(day)

	conn.close()
	

if __name__ == "__main__":
	main()




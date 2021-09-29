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
PERCTEMP = 0.7

# number of days to look ahead in the forecast for alerts
LOOKAHEAD = 7

# filter out days if there is any rain forecast
RAINY = False

# number of days to look back for the average alerts, True = maximum
# TODOLOOKBACK = True

# median/mean for the alert
# TODO

# icons or text
# TODO


VCKEY = 'L69PGR8DVXWM7RZV3DQC4AVRW'

manual_city = 'Boscastle'
manual_latlng = '50.684021,-4.692920'


def weather_scale(wx_type_list):
    """
    wx_type to be assessed ,returns details on them
    returns an integer from 1-5 for a relative scale of the various weather descriptions
    more documents here
    https://www.visualcrossing.com/resources/documentation/weather-api/weather-condition-fields/"""
    
    wx={ 
        'type_2': {'type': 2, 'description': 'Drizzle', 'rating': 1},
        'type_2': {'type': 2, 'description': 'Drizzle', 'rating': 1},
        'type_3': {'type': 3, 'description': 'Heavy Drizzle', 'rating': 1},
        'type_4': {'type': 4, 'description': 'Light Drizzle', 'rating': 1},
        'type_6': {'type': 6, 'description': 'Light Drizzle/Rain', 'rating': 1},
        'type_26': {'type': 26, 'description':'Light Rain', 'rating': 1},
        'type_27': {'type': 27, 'description':'Sky Coverage Decreasing', 'rating': 1},
        'type_28': {'type': 28, 'description':'Sky Coverage Increasing', 'rating': 1},
        'type_29': {'type': 29, 'description':'Sky Unchanged', 'rating': 1},
        'type_41': {'type': 41, 'description':'Overcast', 'rating': 1},
        'type_42': {'type': 42, 'description':'Partially cloudy', 'rating': 1},
        'type_43': {'type': 43, 'description':'Clear', 'rating': 1},
	      'type_1': {'type': 1, 'description':'Blowing Or Drifting Snow','rating': 2},
	      'type_5':	{'type': 5, 'description':'Heavy Drizzle/Rain', 'rating': 2},
	      'type_8':	{'type': 8, 'description':'Fog', 'rating': 2},
	      'type_9':	{'type': 9, 'description':'Freezing Drizzle/Freezing Rain', 'rating': 2},
	      'type_11':	{'type': 11, 'description':'Light Freezing Drizzle/Freezing Rain', 'rating': 2},
	      'type_12':	{'type': 12, 'description':'Freezing Fog', 'rating': 2},
	      'type_14':	{'type': 14, 'description':'Light Freezing Rain', 'rating': 2},
	      'type_17':	{'type': 17, 'description':'Ice', 'rating': 2},
	      'type_18':	{'type': 18, 'description':'Lightning Without Thunder', 'rating': 2},
	      'type_19':	{'type': 19, 'description':'Mist', 'rating': 2},
	      'type_20':	{'type': 20, 'description':'Precipitation In Vicinity', 'rating': 2},
	      'type_23':	{'type': 23, 'description':'Light Rain And Snow', 'rating': 2},
	      'type_24':	{'type': 24, 'description':'Rain Showers', 'rating': 2},
	      'type_31':	{'type': 31, 'description':'Snow', 'rating': 2},
	      'type_32':	{'type': 32, 'description':'Snow And Rain Showers', 'rating': 2},
	      'type_33':	{'type': 33, 'description':'Snow Showers', 'rating': 2},
	      'type_35':	{'type': 35, 'description':'Light Snow', 'rating': 2},
	      'type_36':	{'type': 36, 'description':'Squalls', 'rating': 2},
	      'type_38':	{'type': 38, 'description':'Thunderstorm Without Precipitation', 'rating': 2},
	      'type_10':	{'type': 10, 'description':'Heavy Freezing Drizzle/Freezing Rain', 'rating': 3},
	      'type_13':	{'type': 13, 'description':'Heavy Freezing Rain', 'rating': 3},
	      'type_16':	{'type': 16, 'description':'Hail Showers', 'rating': 3},
	      'type_21':	{'type': 21, 'description':'Rain', 'rating': 3},
	      'type_22':	{'type': 22, 'description':'Heavy Rain And Snow', 'rating': 3},
	      'type_25':	{'type': 25, 'description':'Heavy Rain', 'rating': 3},
	      'type_34':	{'type': 34, 'description':'Heavy Snow', 'rating': 3},
	      'type_37':	{'type': 37, 'description':'Thunderstorm', 'rating': 3},
	      'type_40':	{'type': 40, 'description':'Hail', 'rating': 3},
	      'type_7':	    {'type': 7, 'description':'Duststorm', 'rating': 4},
	      'type_15':	{'type': 15, 'description':'Funnel Cloud/Tornado', 'rating': 4},
	      'type_39':	{'type': 39, 'description':'Diamond Dust','rating': 4},
	      'type_30':	{'type': 30, 'description':'Smoke Or Haze',  'rating': 4},
	}

    results = []
    for i in wx_type_list.split(','):
        rating = next(val for key, val in wx.items() if i.strip() in key)
        results.append(rating['rating'])
    return results


def get_historical():
    """
    gets the historical data for the previous few weeks
    and returns the average temp for that period
    """

    try:
        wx = (requests.get(
            f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?aggregateHours=24&combinationMethod=aggregate&period=last30days&maxStations=-1&maxDistance=-1&contentType=json&unitGroup=metric&locationMode=single&key={VCKEY}&dataElements=default&locations={manual_latlng}&lang=id'))
        wx = wx.json()

    except requests.HTTPError:
        return False

    try:

        daily_data = {}

        maxtemp = 0
        wxrating = 0
        counter = 0

        for item in wx['location']['values']:

            counter += 1
            maxtemp += item['maxt']
            for i in weather_scale(item['conditions']):
                wxrating += int(i)

        average_maxtemp = maxtemp / counter
        average_rating = wxrating / counter

        return round(average_maxtemp, 2), round(average_rating, 2)

    except requests.HTTPError:
        return requests.HTTPError


def get_forecast():
    """
    gets the weather forecast (WX) for the comping period, returns a dictionary with an index
    """

    try:
        wx = (requests.get(
            f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?aggregateHours=24&combinationMethod=aggregate&contentType=json&unitGroup=metric&locationMode=single&key={VCKEY}&dataElements=default&locations={manual_latlng}&lang=id'))
        wx = wx.json()
    except requests.HTTPError:
        return False

    daily_data = {}

    counter = 0

    for item in wx['location']['values']:

        daily_data[counter] = {}
        daily_data[counter]['temp'] = item['temp']
        daily_data[counter]['maxt'] = item['maxt']
        daily_data[counter]['conditions'] = item['conditions']
        daily_data[counter]['rating'] = weather_scale(item['conditions'])
        daily_data[counter]['date'] = datetime.fromtimestamp(
            item['datetime'] / 1000).strftime('%a %-d %b')

        counter += 1

    return daily_data

def compare_temp(average, forecast):
    """compares the average for the past period
    with each coming period and prints it if it exceeds the
    threshold, which is controlled by PERCTEMP

    will only return results if there isn't a rainy day forecast depending on the RAINY setting
     """

    limit = int(average * PERCTEMP)

    results = []

    for i in forecast.items():
        if int(i[0]) < int(LOOKAHEAD):
            if int(i[1]['maxt']) > limit:
                if RAINY and 'rain' not in str(i[1]['conditions']).lower():
                    results.append(i[1]['date'] +
                               ' temp: ' +
                               str(i[1]['temp']) +
                               ' ' +
                               str(i[1]['rating']))
                else:
                    results.append(i[1]['date'] +
                               ' temp: ' +
                               str(i[1]['temp']) +
                               ' ' +
                               str(i[1]['rating']))

    if results:
        return results
    else:
        return False

def main():

    average, number = get_historical()
    forecast = get_forecast()

    alert = compare_temp(average, forecast)
    if alert:
        print('WX!')
        print('---')
        print('WX for ' + manual_city)
        print('historical average: ' + str(average))
        print('---')
        print('Forecast')
        for i in alert:
            print(i)
    
    # print(weather_scale('type_2, type_3, type_31'))

if __name__ == "__main__":
    main()

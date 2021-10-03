import requests
from datetime import datetime

# CONFIG

# threshold that the temp must break in order to get an alert, higher threshold for rainy day
RAINY_PERCTEMP = 1.1
CLEAR_PERCTEMP = 0.75

# number of days to look ahead in the forecast for alerts
LOOKAHEAD = 8

# filter out days if there is any rain forecast
RAINY = True

# number of days to look back for the average alerts, True = maximum
# TODOLOOKBACK = True

# median/mean for the alert
# TODO

# icons or text
# TODO


VCKEY = 'L69PGR8DVXWM7RZV3DQC4AVRW'

manual_city = 'Boscastle'
# manual_latlng = '50.684021,-4.692920'

def get_wx_icon(icon_code):
  if icon_code == 0:
    icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAmVBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjHWqVAAAAMnRSTlMAAQIDBAUGCAoMFxgZHR4hIiU0NTc4QEFFRlhZZmeGh4qLra6xtL/AwdDR1tnb3Pf4+RkSsW4AAACvSURBVHgBJczZWqJgAADQw7+AouOMU2lGtrgYQhny/g/X9+XtuTgUhGDdZ0IC01JpO1YSCsnrJUabnWz+PiGohwM58m/4jEiW94uP4drWd8coIJuN56bpxoVQBrmiPUN3Av24i9cnVaUZ0uZ5bbXd5Gtzg7Afe3DqoGup8u+zuKW1jCAe/9ftMJz+PCwlxK/vv4TEYZgJTN7msv2jEC8vkgJJNW6V8hSkQO5XQqDwAzg9DY/cb+9eAAAAAElFTkSuQmCC'
#   elif icon_code == 'clear-night':
#     icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAmVBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjHWqVAAAAMnRSTlMAAQIDBAUGBxMVFycoKSosMDE/QEpLTFhkZ2prdHZ6ipagoayusLS5u7zGyeXs8vn6+7VdeBQAAACGSURBVHjabU+HDoJQDLxKVRwo4saNgnv1/z/Oiy9PEkOTjrtuVEugqrUSiosDjwnHu3wdekZQP9m1eNjIMbT7d4d+Y32wmBrZEI0mZraCAtTFXUQxtRSCL5GSENy2DrOlawnQswGn+aGvCO1nzJxfe7bL0ebQ8rBJdli2IL/Txbm/5wTV8gEi7AeTMvh8mQAAAABJRU5ErkJggg=='
  elif icon_code == 2:
    icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA5klEQVQoFQXBMSuFYRgA0PO870cGlMFgUEpEBiuKgUGMdhmU5AfIbvYHlNGghCIpLBaUWSmDQSbdgdW9j3MChDRkWbdH4+Z8OvGl6AAFu9Kvb+nPq5a0iQoNtqRtRZg3DPakRVSgZR8AVeDKMypMSdNohKqgC6vSLHDgS0UAoOLBPQVLLrR1SQAUXJikwY9BFI3URlEUTGgBG9IMoGoAC9I2BI6lS6fWwJhrL9IRggDrbr1JT26kD4dWQEAIwIpzZ3YARQDQaBQwAbpVoAI6OqDfuz53QhsoAAgM6DGCBAAAAqN6EQD/vPo8tMz6bZYAAAAASUVORK5CYII='
  elif icon_code == 4:
    icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA40lEQVQoFQXBsSqFYRgA4Of9vv+4AHWUIhORwYqiMIjZKoMSNyC72Q0oo0EZTh1ZZFGSsigpE0omncKK1/MECGnQsj43xsx6c+Jd8QcU7ErfPqQfj3rSJio02JK2FWHOMNiTFlGBnn0AVIEzt6gwKU2hEaqCFlalGeDAu4oAQMWVSwqWdPxqSQAUdEzQ4EsbRSP9oigKxvWADWkaUDWAeWkbAsdS16k1MOrcnXSEIMC6C0/Sua704tAKCAgBeJau7QCKAKCFfvceAC0VAKBgxBAIAACggAVLCAAACAz49KqNAvwDhLU7zZRMOIUAAAAASUVORK5CYII='
  elif icon_code == 3:
    icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA6klEQVQoFQXBry+FYRgA0PO873cVqiCoxgQVG4FwN1E3wWaiZIImEzXJBGN2N6aYovjxBxjdJLuBZO7ncU6AkMZ0DXkwYd67Mx+KP6BgR/r2KQ286EsbqNBgU9pShAXjYFdaQgX69gFQBa49ocK0NINGqAo6WJHmgAMfKgIAFffuKFjW0+pIABT0TNHgyyiKRmpRFAWT+sC6NAuoGsCitAWBU+nKhVUw4dKzdIwgwJpbr9KjGymd6IIIBBKs2DDi3IxtrepPAjSqAHBoHAENYCB0tEL4NawFKCAwak+rNcCbHwAgMOYIBQDgH8ebRS21EV3JAAAAAElFTkSuQmCC'
#   elif icon_code == 'wind':
    # icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAflBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCtoPsAAAAKXRSTlMAAQIDBAUOGx8kJjE7PkVHS05camtvdneHiY+su8DBw8rU1dzm8PH6/PnPEUAAAABvSURBVHgBlc3XDoJgDEDh0+HAvQc4FBHt+7+gI8T8XvJdnKRpk9KSKykB7G/uzjMSRj9ijTRrc2MftweYvxnAJKa9oNPcjw+zYSzOd+pTvtnmxzquI3bPy4BlUVZVWawyEJyEKvaJu4J+y++l0MYLmKUFUAQQSQkAAAAASUVORK5CYII='
#   elif icon_code == 'fog':
#     icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA7UlEQVQoFQXBzyqEURwA0HPv/SazYGGh7NiwUzOlFHv5s1BWnmAW8wBW3gHlGSyUPIBkQcNkY+ElhEgyDb7v5xyAAiCBpAAJJGHJptqGZR+OHaGogYwD4dnIQN+J8KSLAgXrQg9tQMeDsIJChXN3SEhaWuDGACWDSa9oq2SNxhROLaKmQl+YAwBcG6KQwNCPLXvOdG3bdyWsokBG24Uw9iKEd/fWUAAymDWj6FiQQQEAAAAgkVDUDu36VIQsNCpvdrxKFQK3Rr5lAFljDAkwb1otAULlUSNrIONS+BNCCL9CDxUJMKGtkQAh+dLAP69nSf8xfn8mAAAAAElFTkSuQmCC'
  elif icon_code == 1:
    icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA70lEQVQoFQXBLUuDURgA0HPvs1cFtVhFHAaTWMVgGgODySKCQQSTSZPFbrEMi8Hgb1gzCDOINruw5EdUGcJg23s9ByAECAFCAECAEGDaFAiAwKaebz/uPfoz0LOBIAsTR56MnDkVBo6dGHt2YCJgVXEOAOBC0QQ63hAqDSE0VDLeXQKfrlEBgAo3vmBXsYIMADIWFftZ26u+UAOAWvjwopWNVAhJApAkgRlDWop1QEiSAKwp2tBVbJs3C2DOgh1FF0juFGMjhzL2DNWKWwkSaGq7Uvz6VnRsWQIpIckmYFlL9qAPQq0kQJYxBgSKGv4BLfNBIGx3s8kAAAAASUVORK5CYII='
#   elif icon_code == 'partly-cloudy-day':
    # icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAABCUlEQVQoFQXBLUjcYRwA4Od9714F56ZYLAbbmAjC4YIoWIzaLNo8kAmbzW5WYTCDa5v25YnBE0SYTTHIYTEsCSIs+MFO/z+fpwYggaKyb0RLUSFlQBI+mNDBG73oWPZeANTRFCYxZBCfhHEAsoJVDZvuPdjSMI0CFAAbwmcrwiZAlvDWjrYTYQGsuDfk2O+sEuZdW3LgBlu+K0LNs3NndPsjHOoHs376569HXwG+qQyDog6KO6dGfUHhxjq6JZD1YNuREaFJ3ZMBhJBkL/5jDJem3MGaMIMu0IVFYRqQYFf4iD4N9Huyh7qaDPBLaLkV2kLbOyQgySo0zblwbsqVHzqyCoAEACAD8Aph71BRnuBbowAAAABJRU5ErkJggg=='
#   elif icon_code == 'partly-cloudy-night':
    # icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA6UlEQVQoFQXBvyqFYRwA4Od93885AxLDySAMkpiUXAByA7LZbTJYnc4iF+HPxC1YLCYGYVJSslDUCYtTzvD9PE8CAJBl1GoAAKAAKEABAFlt0rY1XZ8SACRZE5tC17uwiwJkGTCkdggOhGUUCmiZsu9VWMW4N/cmkGHGnRB6Tl0IGzp+QYZhPx6t2NACbaHvBA1gT18CNCTsCJfIwJEHNBUJSYVjT0iQ3Zoz4g8JYQDPRhHAkjANGFAw6NsZKqD4cGXIrAXQFl6MIQMs+hJCOHcjdFTIQJLVmtb1zNvSdeAaWQ1AAQBUEgD/3uo/+JyzvikAAAAASUVORK5CYII='
  else:
    icon = ''

  return icon

def weather_scale(wx_type):
    """
    returns an integer from 1-5 for a relative scale of the various weather descriptions
    more documents here
    https://www.visualcrossing.com/resources/documentation/weather-api/weather-condition-fields/"""
    
    wx={ 
        'type_43': {'type': 43, 'description':'Clear', 'rating': 0},
        'type_27': {'type': 27, 'description':'Sky Coverage Decreasing', 'rating': 0},
        'type_28': {'type': 28, 'description':'Sky Coverage Increasing', 'rating': 0},
        'type_29': {'type': 29, 'description':'Sky Unchanged', 'rating': 0},
        
        'type_42': {'type': 42, 'description':'Partially cloudy', 'rating': 0},

        'type_2': {'type': 2, 'description': 'Drizzle', 'rating': 1},
        'type_3': {'type': 3, 'description': 'Heavy Drizzle', 'rating': 1},
        'type_4': {'type': 4, 'description': 'Light Drizzle', 'rating': 1},
        'type_6': {'type': 6, 'description': 'Light Drizzle/Rain', 'rating': 1},
        'type_26': {'type': 26, 'description':'Light Rain', 'rating': 1},
        'type_41': {'type': 41, 'description':'Overcast', 'rating': 1},
        
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

    number = []
    description = []
    for i in wx_type.split(','):
        rating = next(val for key, val in wx.items() if i.strip() == key)
        number.append(rating['rating'])
        description.append(rating['description'])
    return number, description

def get_wx(latlong, type):
    """
    gets the historical data for the previous few weeks
    and returns the average temp for that period
    """
    if type == 'forecast':
        url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?aggregateHours=24&combinationMethod=aggregate&contentType=json&unitGroup=metric&locationMode=single&key={VCKEY}&dataElements=default&locations={latlong}&lang=id'
        
    if type == 'historical':
        url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?aggregateHours=24&combinationMethod=aggregate&period=last30days&maxStations=-1&maxDistance=-1&contentType=json&unitGroup=metric&locationMode=single&key={VCKEY}&dataElements=default&locations={latlong}&lang=id'

    try:
        wx = (requests.get(url))
        wx = wx.json()
        print(wx)
        # if wx['errorCode']:
        #     print(wx)
        #     return False, False

    except requests.HTTPError:
        return False, False

    try:

        daily_data = {}

        maxtemp = 0
        counter = 0

        for item in wx['location']['values']:

            daily_data[counter] = {}
            daily_data[counter]['temp'] = item['temp']
            daily_data[counter]['maxt'] = item['maxt']
            daily_data[counter]['conditions'] = item['conditions']
            daily_data[counter]['rating'],daily_data[counter]['description'] = weather_scale(item['conditions'])
            daily_data[counter]['date'] = datetime.fromtimestamp(
                item['datetime'] / 1000).strftime('%a %-d %b')

            counter += 1
            maxtemp += item['maxt']

        average_maxtemp = round((maxtemp / counter),2)

        return daily_data, average_maxtemp

    except requests.HTTPError:
        return requests.HTTPError


def historical_conditions(daily_data):
    """takes in a dict of the past data and 
    pulls out the conditions and returns 
    an ordered list from most old to new the daily rating from 0-5 (0 best)
    will accept a list and only return the max(ie worst, as forecast include 2"""
    wx = []

    for day in daily_data.items():
        #converts the "type" rating into a dict of the conditions
        rating = weather_scale(day[1]['conditions'])
        #appends the number value for the rating from 1-5    
        wx.append(max(rating))
    return wx

def compare_temp(average, forecast):
    """compares the average for the past period
    with each coming period and prints it if it exceeds the
    threshold, which is controlled by PERCTEMP

    will only return results if there isn't a rainy day forecast depending on the RAINY setting
     """

    results = []

    for i in forecast.items():
        
        #checks if too far in the future
        if int(i[0]) < int(LOOKAHEAD):
 
            #checks for a clear day with rating = 0, and temp above clear day threshold
            if int(i[1]['rating'][0]) == 0 and int(i[1]['maxt']) > int(average * CLEAR_PERCTEMP):
                results.append(i[1]['date'] +
                           ' temp: ' +
                           str(i[1]['maxt']) +
                           ' ' +
                           str(i[1]['description']))
                

            #otherwise checks the day is above the rainy day threshold
            elif int(i[1]['maxt']) > int(average * RAINY_PERCTEMP):
            
                results.append(i[1]['date'] +
                           ' temp: ' +
                           str(i[1]['maxt']) +
                           ' ' +
                           str(i[1]['description']))
                



    if results:
        return results
    else:
        return False

def main(location):

    hist_daily, hist_average_maxtemp = get_wx(location, 'historical')
    forecast_daily, forecast_average_maxtemp = get_wx(location, 'forecast')

    alert = compare_temp(hist_average_maxtemp, forecast_daily)
    
    return alert
    

    
    # if weather_scale('type_2, type_3,type_4,type_30') == [1, 1, 1, 4] and weather_scale('type_21') == [3]:
    #     pass
    # else:
    #     print('weather_scale error')

    # print(weather_scale('type_2, type_30'))
    # print(hist_daily[1]['conditions'])
    # print(historical_conditions(hist_daily))
    # print(historical_conditions(forecast_daily))

if __name__ == "__main__":
    main('london')

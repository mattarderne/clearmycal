# clearmycal
An alerting system to let you know if the weather is going to be "relatively great" in the next 7 days. 

Why: This inspired by someone who, if there is a great day forecast, will cancel all their meetings on that day. So far this only provides alerts using the maxTemp for a day.

About: 

* This is an [xbar](https://xbarapp.com/) plugin, 
* This uses the [VisualCrossing](https://www.visualcrossing.com/resources/documentation/weather-api/how-to-replace-the-dark-sky-api/) weather API


## Todo
1. Compare different types of weather instead of just temperature. [Asking here](https://github.com/nrkno/yr-weather-symbols/issues/21#issuecomment-740599546) but might need to just make a best get


## Requirements

1. VisualCrossing](https://www.visualcrossing.com/resources/documentation/weather-api/how-to-replace-the-dark-sky-api/) API key
1. Requires [xbar](https://xbarapp.com/) to be installed, and `visualcrossing.12h.py` to be copied to the folder

Test with `python visualcrossing.12h.py`

The `.12h.py` indicates to the xbar app how often to run the code. 

# clearmycal
An alerting system to let you know if the weather is going to be "relatively great" in the next 7 days. 

Why: This inspired by someone who, if there is a great day forecast, will cancel all their meetings on that day. 

Currently provides an alert when the upcoming maxTemp for a day exceeds the average over the previous 2 weeks by 25% _(NB: doesn't yet consider wind/rain!)_

**About** 

* This is an [xbar](https://xbarapp.com/) plugin, 
* This uses the [VisualCrossing](https://www.visualcrossing.com/resources/documentation/weather-api/how-to-replace-the-dark-sky-api/) weather API


## Requirements

1. [VisualCrossing](https://www.visualcrossing.com/) API key added to `~/.env` as `visualcrossing` and the `LOCATION` variable to be added to the code. Test this on Visualcrossing
1. Requires [xbar](https://xbarapp.com/) to be installed, and `clearmycal.12h.py` to be copied to the folder

Test with `python clearmycal.12h.py`

The `.12h.py` indicates to the xbar app how often to run the code. 

## Todo
1. Compare different types of weather instead of just temperature. [Asking here](https://github.com/nrkno/yr-weather-symbols/issues/21#issuecomment-740599546) but might need to just make a best guess. Also see [open-meteo](https://open-meteo.com/en/docs#api-documentation) WMO Weather interpretation codes (WW)
1. number of days to look ahead in the forecast for alerts
1. median/mean for the alert
1. icons or text
1. error messages for credit limit and API key
1. [email](https://sendgrid.com/pricing/) notifications and check [calendar](https://developers.google.com/calendar/api/quickstart/python)
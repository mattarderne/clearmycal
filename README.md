# clearmycal
An alerting system to let you know if the weather is going to be "relatively great" in the next 7 days. Darksky API doesn't allow historic access, so history needs to be saved and compared against the coming week.

Why: This inspired by someone who, if there is a great day forecast, will cancel all their meetings on that day. So far this only provides alerts using the maxTemp for a day.

About: This is an [xbar](https://github.com/matryer/xbar-plugins) plugin


## Todo
1. Migrate to a new API [Visual eg](https://www.visualcrossing.com/resources/documentation/weather-api/how-to-replace-the-dark-sky-api/) 
1. Compare different types of weather instead of just temperature. [Asking here](https://github.com/nrkno/yr-weather-symbols/issues/21#issuecomment-740599546) but might need to just make a best get


## Requirements

1. Darkspy API key...  [no longer available](https://darksky.net/dev)  thanks apple!
1. The app will need to run for a few days to build up a base-line before it starts being useful
1. All standard Python3 packages?

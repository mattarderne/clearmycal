# clearmycal
An alerting system to let you know if the weather is going to be "relatively great" in the next 7 days. This inspired by someone who once said that if there is a great day forecast, they will cancel all their meetings. This sounded like a good plan to be automated. So far this only provides alerts using the temp.

An [xbar](https://github.com/matryer/xbar-plugins) plugin

Requires an ordered list of weather icons. [Asking here](https://github.com/nrkno/yr-weather-symbols/issues/21#issuecomment-740599546) but might need to just make a best get

## Todo
Migrate to a new API [Visual eg](https://www.visualcrossing.com/resources/documentation/weather-api/how-to-replace-the-dark-sky-api/)

## Requirements

1. Darkspy API key... get yours at https://darksky.net/dev (API ends end of 2022 thanks apple)
1. The app will need to run for a few days to build up a base-line before it starts being useful
1. packages
```
import requests
import json
from random import randint
import datetime
from datetime import datetime
import sqlite3
import os
```

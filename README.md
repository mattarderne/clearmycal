# clearmycal
An alerting system to let you know if the weather is going to be "relatively great" in the next 7 days

An [xbar](https://github.com/matryer/xbar-plugins) plugin

Requires an ordered list of weather icons. [Asking here](https://github.com/nrkno/yr-weather-symbols/issues/21#issuecomment-740599546) but might need to just make a best get


## Requirements

1. Darkspy API key... get yours at https://darksky.net/dev (they may be stopping the API)
2. packages
```
import requests
import json
from random import randint
import datetime
from datetime import datetime
import sqlite3
import os
```

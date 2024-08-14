#!/bin/python3

## move file into crontab/daly

import os
import requests as rq

api = "https://api.sunrise-sunset.org/json?lat=57.4870365&lng=12.5616751&tzid=Europe/Stockholm&date=today&formatted=0"

stringTime = rq.get(api).json()['results']['sunrise'].split("T")[1].split(":")
activeHour = int(stringTime[0])
activeMin = int(stringTime[1])

deaktive = rq.get(api).json()['results']['sunrise'].split("T")[1].split(":")[0]

aktivefile = open("/home/automate/sunset_file", "w")
aktivefile.write(f"{activeHour}:{activeMin}")
aktivefile.close()

deaktivefile = open("/home/automate/sunrise_file", "w")
deaktivefile.write(deaktive)
deaktivefile.close()

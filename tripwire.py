#!/bin/python3

from gpiozero import Device, DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
import requests as rq
import time
import os

debug = "no"

on = '{"on":true}' # shorten calls
off = '{"on":false}'
headers = {"Content-Type": "application/json"}

api = "https://api.sunrise-sunset.org/json?lat=57.4870365&lng=12.5616751&tzid=Europe/Stockholm&date=today&formatted=0"

ip = (open("ip","r")).read().rstrip() # format "http://ip:port/api/apikey/"

timer = 99999999999 # place holder
aliveMin = 5
aliveTimer = (60 * aliveMin) #change to minuts sleep
plusOnly = 90000 # place holder


# ultrasonic distins to the wall
activationRange = 80 #cm

loop = 0 # for the looks

# raspberry pi gpio stuffs
Device.pin_factory = PiGPIOFactory()
ultrasonic = DistanceSensor(echo=27, trigger=17, max_distance=2)

# this is not very dynamic :/ but it does the job. memory
saveState = [False, False, False]
saveSelf = [False, False, False]

activeHour = 22
activeMin = 00

inActiveTime = 5

def get_sunset():
    global activeHour
    global activeMin
    activeHour = int((open("sunset_file","r")).read().rstrip().split(":")[0])
    activeMin = int((open("sunset_file","r")).read().rstrip().split(":")[1])

def get_sunrise():
    global inActiveTime
    inActiveTime = int((open("sunrise_file","r")).read().rstrip())


def timeUpdate():
    get_sunset()
    get_sunrise()


def lightStatus(light, mode ):
    return rq.get(f"{ip}{mode}/{light}/").json()["state"]["on"]

def sendData(url, data = "{}"):
    rq.put(url, data=data, headers=headers)

def url(group, scene = "off" ):
    if scene != "off":
        url = f"{ip}groups/{group}/scenes/{scene}/recall"
    else:
        url = f"{ip}groups/{group}/action"
    return url

def kitchen(scene): # smart lightbulb
    index = 0
    group = 1
    light = 3
    if lightStatus(light, "lights") != saveState[index]:
        saveState[index] = False

    if not lightStatus(light, "lights") and not saveState[index] and scene != "off" or saveSelf[index] and scene != "off": # some magic, checking if the light is turned on so it doesnt turned it off after counter
        sendData(url(group, scene))
        saveSelf[index] = True
        return
    if scene == "off" and not saveState[index] and saveSelf[index]:
        sendData(url(group), off)
        saveSelf[index] = False
        return
    else:
        saveState[index] = True
        return

def frontDoor(scene): # smart lightbulb

    index = 1
    group = 10
    light = 2
    if lightStatus(light, "lights") != saveState[index]:
        saveState[index] = False

    if not lightStatus(light, "lights") and not saveState[index] and scene != "off" or saveSelf[index] and scene != "off":
        sendData(url(group, scene))
        saveSelf[index] = True
        return
    if scene == "off" and not saveState[index] and saveSelf[index]:
        sendData(url(group), off)
        saveSelf[index] = False
        return
    else:
        saveState[index] = True
        return

def tvRoom(scene): # smart relay

    index = 2
    group = 7
    light = 5
    if lightStatus(light, "lights") != saveState[index]:
        saveState[index] = False

    if not lightStatus(light, "lights") and not saveState[index] and scene != "off" or saveSelf[index] and scene != "off":
        sendData(url(group), on)
        saveSelf[index] = True
        return
    if scene == "off" and not saveState[index] and saveSelf[index]:
        sendData(url(group), off)
        saveSelf[index] = False
        return
    else:
        saveState[index] = True
        return

def all_lamps(scene):

    print(scene)
    if scene == "on":
        print("all lampts are doing things")
        tvRoom(scene)
        time.sleep(1)
        kitchen(1)
        time.sleep(1)
        frontDoor(1)
    else:
        frontDoor(scene)
        frontDoor(2)
        time.sleep(2)
        frontDoor(scene)
        kitchen(scene)
        kitchen(2)
        time.sleep(3)
        kitchen(scene)
        tvRoom(scene)

def log(timeStamp):

    logFile = open("log", "a")
    logFile.write(f"{timeStamp}\n")
    logFile.close()

def fancyLop(loop):

    os.system('cls' if os.name == 'nt' else 'clear')
    #print("\n" * 10)
    print(".=" * loop * loop + ".")
    if loop > 5:
        loop = 0
    loop = loop + 1
    return loop

print("starting loop :) HF <3")
try:
    if debug == "yes":
         print(saveSelf)
         time.sleep(2)
         all_lamps("on")
         time.sleep(2)
         all_lamps("on")
         print(saveSelf)
         time.sleep(2)
         all_lamps("off")
         print(saveSelf)

    else:

        while True:

            cm = int(ultrasonic.distance * 100)
            rightNow = int(time.time())
            currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            currentMin = int(time.strftime("%M", time.localtime()))
            currentHour = int(time.strftime("%H", time.localtime()))
            plusOnly = timer - rightNow
            if plusOnly > 0 and plusOnly <= aliveTimer:
                print(plusOnly)

            if cm < activationRange:

                print(f"{currentTime} some one walked past {cm} cm")
                log(currentTime)

                timeUpdate()

                if (currentHour > activeHour or currentHour == activeHour and currentMin >= activeMin) or currentHour <= inActiveTime:
                    timer = rightNow + aliveTimer
                    all_lamps("on")
                time.sleep(1)

            elif timer <= rightNow:

                timer = 99999999999
                all_lamps("off")

            #loop = fancyLop(loop) #just for looks :)
            time.sleep(0.1)

except KeyboardInterrupt:
    #all_lamps("off")
    print ("\nexit")

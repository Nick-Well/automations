#!/bin/python3

from gpiozero import Device, DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
import requests as rq
import time
import os


on = '{"on":true}' # shorten calls
off = '{"on":false}'
headers = {"Content-Type": "application/json"}

ip = (open("ip","r")).read().rstrip() # format "http://ip:port/api/apikey/"

timer = 99999999999 # place holder
aliveMin = 5
aliveTimer = (60 * aliveMin) #change to minuts sleep
plusOnly = 90000 # place holder

activeTime = 22 # at what time the tripwire is active
inActiveTime = 4 # intill

# ultrasonic distins to the wall
activationRange = 80 #cm

loop = 0 # for the looks

# raspberry pi gpio stuffs
Device.pin_factory = PiGPIOFactory()
ultrasonic = DistanceSensor(echo=27, trigger=17, max_distance=2)

# this is not very dynamic :/ but it does the job. memory
saveState = [False, False, False]
saveSelf = [False, False, False]


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

    group = 1
    if not lightStatus(2, "lights") and not saveState[0] and scene != "off" or saveSelf[0] and scene != "off": # some magic, checking if the light is turned on so it doesnt turned it off after counter
        sendData(url(group, scene))
        saveSelf[0] = True
        return
    if scene == "off" and not saveState[2] and saveSelf[0]:
        sendData(url(group), off)
        saveSelf[0] = False
        return
    else:
        saveState[0] = True
        return

def frontDoor(scene): # smart lightbulb

    group = 10
    if not lightStatus(6, "lights") and not saveState[1] and scene != "off" or saveSelf[1] and scene != "off":
        sendData(url(group, scene))
        saveSelf[1] = True
        return
    if scene == "off" and not saveState[2] and saveSelf[1]:
        sendData(url(group), off)
        saveSelf[1] = False
        return
    else:
        saveState[1] = True
        return

def tvRoom(scene): # smart relay

    group = 7
    if not lightStatus(5, "lights") and not saveState[2] and scene != "off" or saveSelf[2] and scene != "off":
        sendData(url(group), on)
        saveSelf[2] = True
        return
    if scene == "off" and not saveState[2] and saveSelf[2]:
        sendData(url(group), off)
        saveSelf[2] = False
        return
    else:
        saveState[2] = True
        return

def all_lamps(scene):

    print(scene)
    if scene == "on":
        print("all lampts are doing things")
        tvRoom(scene)
        time.sleep(1)
        kitchen(3)
        time.sleep(1)
        frontDoor(2)
    else:
        frontDoor(scene)
        frontDoor(1)
        time.sleep(2)
        frontDoor(scene)
        kitchen(scene)
        kitchen(2)
        time.sleep(2)
        kitchen(scene)
        tvRoom(scene)

def log(timeStamp):

    logFile = open("log", "a")
    logFile.write(f"{timeStamp}\n")
    logFile.close()

def fancyLop(loop):

    os.system('cls' if os.name == 'nt' else 'clear')
    print(".=" * loop * loop + ".")
    if loop > 5:
        loop = 0
    loop = loop + 1
    return loop

print("starting loop :) HF <3")

try:
    while True:

        cm = int(ultrasonic.distance * 100)
        rightNow = int(time.time())
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        currentHour = int(time.strftime("%H", time.localtime()))
        plusOnly = timer - rightNow
        if plusOnly > 0 and plusOnly <= aliveTimer:
            print(plusOnly)

        if cm < activationRange:
            print(f"{currentTime} some one walked past {cm} cm")
            log(currentTime)
            if currentHour >= activeTime or currentHour <= inActiveTime:
                timer = rightNow + aliveTimer
                all_lamps("on")
            time.sleep(1)

        elif timer <= rightNow:
            timer = 99999999999
            all_lamps("off")
        #loop = fancyLop(loop) #just for looks :)
        time.sleep(0.1)

except KeyboardInterrupt:
    print ("\nexit")

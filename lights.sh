#!/bin/bash

ip=$(cat ./ip)
memoryday=0
memoryKitchen=true
nightKitchen=true
memoryVardagsrummet=true


kitchen(){
  curl --request PUT -H 'Content-Type: application/json' --data '{}'  "${ip}1/scenes/$1/recall"
}
kitchenOff(){
  curl --request PUT -H 'Content-Type: application/json' --data '{"on":false}'  "${ip}1/actiona"
}
middag(){
  kitchen 2
}
onelight(){
  kitchen 3
}
turnoffLight(){
  middag
  sleep 10
  kitchenOff
}
vardagsrummet(){
  curl --request PUT -H 'Content-Type: application/json' --data '{"on":true}'  "${ip}4/action"
}

sunset_get=$(curl -s "https://api.sunrise-sunset.org/json?lat=57.4870365&lng=12.5616751&tzid=Europe/Stockholm&formatted=1&date=today" | jq -r '.results.sunset')
sunset=$sunset_get
sunsetampm=$(echo $sunset | awk '{print $2;}')
sunseth=$(echo $sunset | awk '{print $1;}'| cut -d ':' -f 1)
sunsetm=$(echo $sunset | awk '{print $1;}'| cut -d ':' -f 2)

while true ; do
  sleep 1
  today=$(date "+%e")
  time=$(date "+%l:%M:%S %p")
  ampm=$(echo $time | awk '{print $2;}')
  timeh=$(echo $time | awk '{print $1;}'| cut -d ':' -f 1)
  timem=$(echo $time | awk '{print $1;}'| cut -d ':' -f 2)

  # köket nattlampa 11:15 pm nattlampa av 3:30 am

  if [ $timeh -eq 11 ] && [ $timem -gt 15 ] && [ $ampm = "PM" ] && $memoryKitchen ; then
    onelight
    memoryKitchen=false
    echo "night light on"
  fi

  if [ $timeh -eq 3 ] && [ $timem -gt 30 ] && [ $ampm = "AM" ] && $nightKitchen ; then
    turnoffLight
    nightKitchen=false
    echo "lights out in kitchen"
  fi

  #if [ $timeh -eq $sunseth ] && [ $timem -gt $sunsetm ] && [ $ampm = "PM" ] && $nightKitchen ; then
  #  onelight
  #  echo "night light is turned on"
  #fi

  #

  if [ $timeh -eq $sunseth ] && [ $timem -gt $sunsetm ] && [ $timeh -lt 9 ] && [ $ampm = "PM" ] && $memoryVardagsrummet ; then
    vardagsrummet
    memoryVardagsrummet=false
    echo "tv room lights active"
  fi

  if [ $memoryday != $today ] ; then
    memoryday=$today
    memoryKitchen=true
    memoryVardagsrummet=true
    echo "all bool are reset and set day to $memoryday"
  fi

done

#!/bin/bash

old_ip=""
firstCheck=0

restartDock(){
  docker stop wg-easy
  docker rm wg-easy
  docker run -d --name=wg-easy -e LANG=se -e WG_HOST=$1 -e PASSWORD=$passwd -v ~/.wg-easy:/etc/wireguard -p 51820:51820/udp -p 51821:51821/tcp --cap-add=NET_ADMIN --cap-add=SYS_MODULE --sysctl="net.ipv4.conf.all.src_valid_mark=1" --sysctl="net.ipv4.ip_forward=1" --restart unless-stopped ghcr.io/wg-easy/wg-easy
}

sendMsg(){
  curl -X POST -H "Content-Type: application/json" 'http://localhost:4322/v2/send' -d '{"message": "'"$1"'", "number": "'"$pNr"'", "recipients": [ "'"$pNr"'" ]}'
}

checkDock(){
  while (! systemctl is-active --quiet docker-d26a05adc3ae7b5978e3362531928843c7c02d504b5cbc3e7b5583e75392ea1a.scope); do
    echo "sleep 5"
    sleep 5
  done
  echo "docker is running"
  sleep 15
}

apiService(){
  url=("https://ifconfig.co/" "https://api.ipify.org" "https://icanhazip.com/" "https://checkip.amazonaws.com/" "https://wtfismyip.com/text")
  numUrl=${#url[@]}
  randomUrl=$((RANDOM % numUrl))
  echo "${url[$randomUrl]}"
}


main(){

  passwd=$(cat ./password)
  pNr=$(cat ./phoneNR)

  #checkDock
  while true ; do
    url=$(apiService)
    ip=$(curl -s $url)
    ip=$(echo $ip | awk '{print $1;}')
    if [ "$ip" = "429" ] || [ "$ip" = "error" ]; then
      ip=$old_ip
      echo "tofast"
      sleep 5
    fi
    sleep 2
    if [ -n "$ip" ] ; then
      if [ "$old_ip" != "$ip" ] ; then
        if [ 0 = $firstCheck ] ; then
          old_ip=$ip
          firstCheck=1
          restartDock $old_ip
          echo "FIRST IP SET IN TO MEMORY"
          sendMsg "started with ip: $old_ip"
        else
          old_ip=$ip
          restartDock $old_ip
          sendMsg $old_ip
        fi
      fi
    else
      echo "no connection to $url"
    fi
  done
}

main

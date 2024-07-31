# automations
im just going to push all my automations in here
Require some docker countaners.

### CheckIPvpn.sh
it checks ip address against a couple api's every now and then. to check that the ip is static.
Sends ip over signal and restarts the wireguard docker with the correct ip.

docker:    bbernhard/signal-cli-rest-api:latest
api's:     ifconfig, api.ipify, icanhazip, checkip.amazonaws, wtfismyip

### lights.sh
turnes on lights att sundown. unless sundown past 10pm

docker:    deconzcommunity/deconz:latest
api:       api.sunrise-sunset

### tripwire.py
ultra sunic "tripwire".
Aktivates lights att night wen passing by the tripwire.

docker:    deconzcommunity/deconz:latest

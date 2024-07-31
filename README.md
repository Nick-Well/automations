# automations
im just going to push all my automations in here
Require some docker countaners.
\n
### CheckIPvpn.sh
it checks ip address against a couple api's every now and then. to check that the ip is static.
Sends ip over signal and restarts the wireguard docker with the correct ip.
\n
docker:    bbernhard/signal-cli-rest-api:latest\n
api's:     ifconfig, api.ipify, icanhazip, checkip.amazonaws, wtfismyip
\n
### lights.sh
turnes on lights att sundown. unless sundown past 10pm
\n
docker:    deconzcommunity/deconz:latest\n
api:       api.sunrise-sunset
\n
### tripwire.py
ultra sunic "tripwire".
Aktivates lights att night wen passing by the tripwire.
\n
docker:    deconzcommunity/deconz:latest

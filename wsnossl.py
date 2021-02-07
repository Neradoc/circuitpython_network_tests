# set debug to False for future imports
#import micropython
#micropython.opt_level(1)

import time
import sys
import json

import wifi
import socketpool
import ssl
import secrets

print("CONNECT WIFI")
wifi.radio.connect(secrets.ssid,secrets.password)
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()

import uwebsockets.client

#print("TESTING SSL WEBSOCKETS")
#url = "wss://echo.websocket.org"
print("TESTING WEBSOCKETS")
url = "ws://echo.websocket.org"
#print("TESTING LOCAL COMPUTER")
#url = "ws://spyromini.local:5000"

ws = uwebsockets.client.connect(url)

message = "Repeat this"
print(f"SENDING:  <{message}>")
ws.send(message)
result = ws.recv()
print(f"RECEIVED: <{result}>")
if result == message:
	print("SUCCESS !!")
else:
	print("OH NO IT WENT WRONG")

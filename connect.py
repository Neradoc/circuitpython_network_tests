#import code_horloge
#import code_wsnossl
#import code_wsyesssl

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

hostname = "echo.websocket.org"
port = 80

addr_info = pool.getaddrinfo(
	hostname, port, 0, pool.SOCK_STREAM
)[0]
sock = pool.socket(
	addr_info[0], addr_info[1], addr_info[2]
)
connect_host = addr_info[-1][0]

r = sock.connect((connect_host,port))


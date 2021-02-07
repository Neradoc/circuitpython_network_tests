import wifi
import socketpool
import ssl
import secrets

import random
import adafruit_binascii as binascii

"""
NOTE: requires the usual secrets.py file

The test
- connects to the server
- sends headers to switch to websockets mode
- waits for the server to send headers back

What's expected from the server:
< HTTP/1.1 101 Web Socket Protocol Handshake
< Connection: Upgrade
< Date: Sat, 06 Feb 2021 22:54:49 GMT
< Sec-WebSocket-Accept: q45sdf1sq5df6qsd4qs6df5=
< Server: Kaazing Gateway
< Upgrade: websocket
<

Different tests available
- LOCAL=False connects to echo.websocket.org
- LOCAL=True connects to LOCALIP running some websockets server
- SSL switches SSL on or off (for non locl tests)
- TIMEOUT allows callling settimeout() (if not False)

## The local server is running:

import asyncio
import websockets

async def do_echo(websocket, path):
    print("Connection from {}".format(websocket.remote_address))
    name = await websocket.recv()
    print("< {}".format(name))

    greeting = "{}".format(name)
    await websocket.send(greeting)
    print("> {}".format(greeting))

print("Starting")
start_server = websockets.serve(do_echo, '0.0.0.0', 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


"""
SSL, LOCAL = (True, False) # wss://echo.websocket.org
SSL, LOCAL = (False, False) # ws://echo.websocket.org
SSL, LOCAL = (False, True) # ws://localip
TIMEOUT = False # not False to set a timeout
LOCALIP = "192.168.1.51" # where you are running a python3 websockets server

print("CONNECT WIFI")
wifi.radio.connect(secrets.ssid,secrets.password)
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()

if SSL:
	port = 443
else:
	port = 80

if LOCAL:
	hostname = LOCALIP
	port = 5000
	SSL = False
else:
	hostname = "echo.websocket.org"

addr_info = pool.getaddrinfo(
	hostname, port, 0, pool.SOCK_STREAM
)[0]
sock = pool.socket(
	addr_info[0], addr_info[1], addr_info[2]
)
connect_host = addr_info[-1][0]

if TIMEOUT != False:
	sock.settimeout(TIMEOUT)

if SSL:
	print("doing SSL")
	sock = ssl_context.wrap_socket(sock,server_hostname = hostname)
	connect_host = hostname

print("URL",(connect_host,port))
r = sock.connect((connect_host,port))

key = binascii.b2a_base64(bytes(random.getrandbits(8) for _ in range(16)))[:-1]

def send_header(header):
	print(">",header)
	sock.send(f"{header}\r\n".encode("utf-8"))

send_header('GET / HTTP/1.1')
send_header(f'Host: {connect_host}:{port}')
send_header(f'Connection: Upgrade')
send_header(f'Upgrade: websocket')
send_header(f'Sec-WebSocket-Key: {key.decode()}')
send_header(f'Sec-WebSocket-Version: 13')
send_header(f'Origin: http://{connect_host}:{port}')
send_header(f'')

buffer =  bytearray(8)
dataString = ""
try:
	while True:
		num = sock.recv_into(buffer,1)
		dataString += str(buffer, 'utf8')[:num]
		if dataString[-2:] == "\r\n":
			print("<",dataString[:-2])
			dataString = ""
		if num == 0:
			print("Zero received")
			break
except Exception as ex:
	print(ex)
	print("BUFFER",buffer)
	print("DATA  ",dataString)
finally:
	sock.close()

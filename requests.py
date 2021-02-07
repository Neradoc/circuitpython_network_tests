import socketpool
import ssl
import sys
import wifi
import adafruit_requests
from secrets import secrets

print("WIFI: Connecting")
#wifi.radio.start_scanning_networks()
wifi.radio.connect(secrets['ssid'],secrets['password'])
#wifi.radio.stop_scanning_networks()
print("WIFI: " + str(wifi.radio.ipv4_address))

# setting up sockets and request
pool = socketpool.SocketPool(wifi.radio)
sslc = ssl.create_default_context()
requests = adafruit_requests.Session(pool, sslc)

urlhttp  = "http://wifitest.adafruit.com/testwifi/index.html"

print("-"*70)
print(f"getting {urlhttp}")
try:
	response = requests.get(urlhttp)
	print(f"{response.status_code}, texte: {response.text}")
except Exception as ex:
	sys.print_exception(ex)

urlhttps = "https://httpbin.org/get"

print("-"*70)
print(f"getting {urlhttps} ax text")
try:
	response = requests.get(urlhttps)
	print(f"{response.status_code}, texte: {response.text}")
except Exception as ex:
	sys.print_exception(ex)

print("-"*70)
print(f"getting {urlhttps} as JSON")
try:
	response = requests.get(urlhttps)
	jason = response.json()
	print(f"{response.status_code}, User Agent: {jason['headers']['User-Agent']}")
except Exception as ex:
	sys.print_exception(ex)

print("-"*70)

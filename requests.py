import wifi
import ssl
import socketpool
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
 
url = "https://httpbin.org/get"

print(f"getting {url} (twice)")

response = requests.get(url)
print(f"{response.status_code}, texte: {response.text}")

response = requests.get(url)
jason = response.json()
print(f"{response.status_code}, User Agent: {jason['headers']['User-Agent']}")

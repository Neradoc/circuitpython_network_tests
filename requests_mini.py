import wifi, socketpool, ssl
import adafruit_requests
from secrets import secrets

wifi.radio.connect(secrets['ssid'],secrets['password'])
pool = socketpool.SocketPool(wifi.radio)
sslc = ssl.create_default_context()
requests = adafruit_requests.Session(pool, sslc)

urlhttp  = "http://wifitest.adafruit.com/testwifi/index.html"
response = requests.get(urlhttp)
print(response.text)

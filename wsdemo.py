import wifi
from secrets import secrets
wifi.radio.connect(ssid=secrets["ssid"], password=secrets["password"])

#import examples.echo_websocket_org
import examples.echo_ssl_websocket_org

# circuitpython_network_tests
Bunch of scripts to test network connections in circuitpython

### connect.py
Just try to connect to echo.websocket.org without SSL

### purehttp.py
Send a simple GET request and print the result, with and without SSL

### requests.py
Send a GET request through adafruit_requests, with and without SSL

### wslocal.py
Connect to a local echo server with websockets and send "Repeat this", display the reply

### wsnossl.py
Connect to ws://echo.websocket.org and send "Repeat this", display the reply

### wsyesssl.py
Connect to wss://echo.websocket.org and send "Repeat this", display the reply

### wsdirect.py
Single file websocket connection test, parameters inside to choose local/websocket.org, SSL or not, set timeout or not.

### wsdirect-hello.py
Add to wsdirect: send a little message and get the response

### echo_server.py
Local echo websockets server (port 5000)

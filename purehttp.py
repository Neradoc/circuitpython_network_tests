import board
import time

#####################################################################

import wifi,ssl,socketpool

print("Connect to WIFI")
wifi.radio.connect("maisongugus","lsldvdlabmcdulm7579")
print(wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
sslc = ssl.create_default_context()

#####################################################################
buffer =  bytearray(32)

def http_get(url):
	global buffer
	_, _, host, path = url.split('/', 3)

	if url.startswith("https"):
		port = 443
	else:
		port = 80

	addr = pool.getaddrinfo(host,port)[0][-1]
	realhost = addr[0]
	s = pool.socket()

	if url.startswith("https"):
		print("HTTPS HOST:",host)
		s = sslc.wrap_socket(s,server_hostname = host)
		realhost = host

	s.settimeout(1)
	s.connect((realhost,port))

	s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
	dataString = ""
	while True:
		num = s.recv_into(buffer,32)
		# print(num,buffer)
		dataString += str(buffer, 'utf8')[:num]
		# if num < len(buffer)
		if num == 0:
			break
	result = dataString.split("\r\n\r\n",1)
	while len(result) < 2:
		result += [""]
	s.close()
	return result

if True:
	# test: télécharger des trucs ou autre
	# http
	url = "http://wifitest.adafruit.com/testwifi/index.html"
	print("#### GET",url)
	_,body = http_get(url)
	print("# HTTP:","<"+body+">")
	# https
	url = "https://gist.githubusercontent.com/Neradoc/1cfb69af112f2ba1408abb3aefe492e9/raw/57caf9fba0d6a1e4fdf568246bb4ccc5d3cdb72c/test_wifi.txt"
	print("#### GET",url)
	_,body = http_get(url)
	print("# HTTPS:","<"+body+">")

print("#"*40)

#####################################################################

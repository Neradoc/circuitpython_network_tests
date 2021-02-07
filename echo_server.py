import asyncio
import websockets

async def do_echo(websocket, path):
	try:
		print("Connection from {}".format(websocket.remote_address))
		name = await websocket.recv()
		print("< {}".format(name))

		greeting = "{}".format(name)
		await websocket.send(greeting)
		print("> {}".format(greeting))
	except Exception as ex:
		print("ERROR",ex)

print("Starting")
start_server = websockets.serve(do_echo, '0.0.0.0', 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

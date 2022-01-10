####################################################
#  Network Programming - Unit 6 Remote Procedure Call          
#  Program Name: 3-RPCServer.py                                      			
#  This program demos a simple RPC server           		
#  Install functions
#  Use 2-RPCClient.py as client program
#  2021.07.21                                                 									
####################################################
from xmlrpc.server import SimpleXMLRPCServer

PORT = 8888

def add(x, y):
	return x + y
		
def subtract(x, y):
	return x - y
		
def multiply(x, y):
	return x * y
		
def divide(x, y):
	return x / y

def main():
	server = SimpleXMLRPCServer(('localhost', PORT))
	server.register_function(add, 'add')
	server.register_function(subtract, 'sub')
	server.register_function(multiply, 'mul')
	server.register_function(divide, 'div')
	print('Listen on port  %d' % PORT)
	try:
		print('Use Control-C to exit!')
		server.serve_forever()
	except KeyboardInterrupt:
		print('Server exit')
# end of main

if __name__ == '__main__':
	main()

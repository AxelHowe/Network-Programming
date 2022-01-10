####################################################
#  Network Programming - Unit 6 Remote Procedure Call          
#  Program Name: 4-RPCServer.py                                      			
#  This program demos a simple RPC server        
#  Register multicall function
# The MultiCall object provides a way to encapsulate multiple calls to a remote server into a single request		
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
	server = SimpleXMLRPCServer(("localhost", PORT))
	print("Listening on port %d..." % PORT)
	server.register_multicall_functions()
	server.register_function(add, 'add')
	server.register_function(subtract, 'sub')
	server.register_function(multiply, 'mul')
	server.register_function(divide, 'div')
	server.serve_forever()
# end of main()

if __name__ == '__main__':
	main()
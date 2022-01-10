####################################################
#  Network Programming - Unit 6 Remote Procedure Call          
#  Program Name: 5-RPCServer.py                                      			
#  This program demos a simple RPC server           		
#  Install an instance with custom dispatch method
#  Use 2-RPCClient.py as client program
#  2021.07.21                                                 									
####################################################
from xmlrpc.server import SimpleXMLRPCServer

PORT = 8888

def add(x, y):
	return x + y
		
def subtract(x, y):
	return x - y
		
class Math:
	def _dispatch(self, method, params):
		if(method == 'add'):
			return add(params[0], params[1])
		elif(method == 'sub'):
			return subtract(params[0], params[1])
		elif(method == 'mul'):
			return params[0] * params[1]
		elif(method == 'div'):
			return params[0] / params[1]
		else:
			raise 'Bad method'
# end of class Math

def main():
	server = SimpleXMLRPCServer(('localhost', PORT))
	server.register_instance(Math())
	print('Listen on port  %d' % PORT)
	try:
		print('Use Control-C to exit!')
		server.serve_forever()
	except KeyboardInterrupt:
		print('Server exit')
# end of main

if __name__ == '__main__':
	main()

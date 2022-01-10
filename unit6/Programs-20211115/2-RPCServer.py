####################################################
#  Network Programming - Unit 6 Remote Procedure Call          
#  Program Name: 2-RPCServer.py                                      			
#  This program demos a simple RPC server           		
#  Install an instance
#  2021.07.21                                                 									
####################################################
from xmlrpc.server import SimpleXMLRPCServer

PORT = 8888

class Calculate:
	def add(self, x, y):
		print('%d + %d = %d' % (x, y, x+y))
		return x + y
		
	def sub(self, x, y):
		print('%d - %d = %d' % (x, y, x-y))
		return x - y
		
	def mul(self, x, y):
		print('%d * %d = %d' % (x, y, x*y))
		return x * y
		
	def div(self, x, y):
		try:
			print('%d / %d = %d' % (x, y, x/y))
		except:
			print('Divide by zero')
		return x / y
# end of class Calculate

def main():
	obj = Calculate()
	server = SimpleXMLRPCServer(('localhost', PORT))
	server.register_instance(obj)
	print('Listen on port  %d' % PORT)
	try:
		print('Use Control-C to exit!')
		server.serve_forever()
	except KeyboardInterrupt:
		print('Server exit')
# end of main

if __name__ == '__main__':
	main()

####################################################
#  Network Programming - Unit 6 Remote Procedure Call          
#  Program Name: 6-MultiThreadRPCServer.py                                      			
#  This program demos a multithreaded RPC server           		
#  2021.08.12                                                 									
####################################################
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import time
import threading

PORT = 8888
EnableCS = False

class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
	pass

class Calculate:
	def __init__(self):
		self.shared_variable = 0
		if(EnableCS):
			self.lock = threading.Lock()
		
	def add(self, x, y):
		print('add() begin')
		time.sleep(5)
		print('%d + %d = %d' % (x, y, x+y))
		return x + y
		
	def sub(self, x, y):
		print('sub() begin')
		time.sleep(2)
		print('%d - %d = %d' % (x, y, x-y))
		return x - y
		
	def mul(self, x, y):
		print('mul() begin')
		time.sleep(5)
		print('%d * %d = %d' % (x, y, x*y))
		return x * y
		
	def div(self, x, y):
		print('div() begin')
		time.sleep(5)
		try:
			print('%d / %d = %d' % (x, y, x/y))
		except:
			print('Divide by zero')
		return x / y
		
	def modify_value(self, val):
		if(EnableCS):
			self.lock.acquire()
			try:
				self.shared_variable += val
				time.sleep(0.1)
				self.shared_variable -= val
			finally:
				self.lock.release()
		else:
			self.shared_variable += val
			time.sleep(0.1)
			self.shared_variable -= val
		return self.shared_variable
	
# end of class Calculate

def main():
	obj = Calculate()
	#server = SimpleXMLRPCServer(('localhost', PORT))
	server = ThreadXMLRPCServer(('localhost', PORT))	
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

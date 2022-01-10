####################################################
#  Network Programming - Unit 6 Remote Procedure Call          
#  Program Name: 2-RPCClient.py                                      			
#  This program demos a simple RPC client           		
#  2021.07.21                                                 									
####################################################
import sys
import xmlrpc.client

PORT = 8888

def main():
	if(len(sys.argv) < 5):
		print("Usage: python3 2-RPCClient.py serverIP cmd x y (cmd: add, sub, mul, div)")
		exit(1)

	x = int(sys.argv[3])
	y = int(sys.argv[4])
	
	server = xmlrpc.client.ServerProxy('http://' + sys.argv[1] + ':' + str(PORT))
	if(sys.argv[2] == 'add'):
		result = server.add(x, y)
		print(str(x) + '+' + str(y) + '=' + str(result))
	elif(sys.argv[2] == 'sub'):
		result = server.sub(x, y)
		print(str(x) + '-' + str(y) + '=' + str(result))
	elif(sys.argv[2] == 'mul'):
		result = server.mul(x, y)
		print(str(x) + '*' + str(y) + '=' + str(result))
	elif(sys.argv[2] == 'div'):
		try:
			result = server.div(x, y)
			print(str(x) + '/' + str(y) + '=' + str(result))
		except:
			print('Divide by zero')
	else:
			print('Usage: python3 2-RPCClient.py serverIP cmd x y (cmd: add, sub, mul, div)')

	
# end of main

if __name__ == '__main__':
	main()

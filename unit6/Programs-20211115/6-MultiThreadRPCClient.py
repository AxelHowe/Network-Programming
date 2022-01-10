####################################################
#  Network Programming - Unit 6 Remote Procedure Call          
#  Program Name: 6-MultiThreadRPCClient.py                                      			
#  This program demos a simple RPC client           		
#  2021.08.12                                              									
####################################################
import sys
import xmlrpc.client

PORT = 8888

def main():
	if(len(sys.argv) < 3):
		print("Usage: python3 6-MultiThreadRPCClient.py serverIP val")
		exit(1)

	server = xmlrpc.client.ServerProxy('http://' + sys.argv[1] + ':' + str(PORT))
	val = int(sys.argv[2])
	
	result = 0
	for i in range(100):
		result += server.modify_value(val)
		print('%dth Result = %d' % (i, result))
	
# end of main

if __name__ == '__main__':
	main()

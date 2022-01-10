####################################################
#  Network Programming - Unit 6 Remote Procedure Call          
#  Program Name: 4-RPCClient.py                                      			
#  This program demos a simple RPC client           
#  Register multicall function		
#  2021.07.21                                                 									
####################################################
import sys
import xmlrpc.client

PORT = 8888

def main():
	if(len(sys.argv) < 4):
		print("Usage: python3 4-RPCClient.py serverIP  x y ")
		exit(1)

	x = int(sys.argv[2])
	y = int(sys.argv[3])

	proxy = xmlrpc.client.ServerProxy('http://' + sys.argv[1] + ':' + str(PORT))
	multicall = xmlrpc.client.MultiCall(proxy)
	multicall.add(x, y)
	multicall.sub(x, y)
	multicall.mul(x, y)
	multicall.div(x, y)
	result = multicall()
	try:
		a1, a2, a3, a4 = tuple(result)
		print("x = %d, y = %d, add=%d, sub=%d, mul=%d, div=%d" % (x, y, a1, a2, a3, a4))
	except:
		print('Divide by zero')
# end of main()

if __name__ == '__main__':
	main()
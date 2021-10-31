####################################################
#  Network Programming - Unit 5  User Datagram Protocol          
#  Program Name: 1-UDPServer.py                                      			
#  This program receives a UDP message and reply a message to client.           		
#  2021.07.15                                                  									
####################################################
import socket

PORT = 8888
BUF_Size = 1024

def main():
	# Create a UDP Server socket
	dgramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Bind 	on any incoming interface with PORT, '' is any interface
	dgramSocket.bind(('', PORT))
	
	print('Waiting on port: %s ' % PORT)
	
	# Receive client message
	client_msg, (rip, rport) = dgramSocket.recvfrom(BUF_Size)
	msg = 'Receive messgae: ' + client_msg.decode('utf-8') + ',from IP: ' + str(rip) + ' port: ' + str(rport)
	print(msg)

	# Reply message
	msg = 'Server reply!!'
	dgramSocket.sendto(msg.encode('utf-8'), (rip, rport))
	print('Send reply message')
	
	# Close the UDP socket
	dgramSocket.close()
# end of main

if __name__ == '__main__':
	main()

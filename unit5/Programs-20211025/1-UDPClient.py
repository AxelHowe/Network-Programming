####################################################
#  Network Programming - Unit 5  User Datagram Protocol          
#  Program Name: 1-UDPClient.py                                      			
#  This program sends a UDP message and waits for a reply .           		
#  2021.07.15                                                  									
####################################################
import sys
import socket

PORT = 8888
BUF_Size = 1024

def main():
	if(len(sys.argv) < 2):
		print("Usage: python3 1-UDPClient.py ServerIP\n")
		exit(1)

	# Get server IP
	serverIP = socket.gethostbyname(sys.argv[1])
	
	# Create a UDP client socket
	dgramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	# Send message
	msg = 'Client hello!!'
	dgramSocket.sendto(msg.encode('utf-8'), (serverIP, PORT))

	# Receive server reply
	srv_msg, (rip, rport) = dgramSocket.recvfrom(BUF_Size)
	msg = 'Receive reply: ' + srv_msg.decode('utf-8') + ',from IP: ' + str(rip) + ' port: ' + str(rport)
	print(msg)

	
	# Close the UDP socket
	dgramSocket.close()
# end of main

if __name__ == '__main__':
	main()

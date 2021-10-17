####################################################
#  Network Programming - Unit 2 Simple TCP Client Server Program         
#  Program Name: 4-TCPServer.py                                      			
#  The program is a simple TCP server. The program test the recv_buf_size.           		
#  2021.07.13                                                   									
####################################################
import socket

PORT = 6666
backlog = 5
BUF_SIZE = 26			# Receive buffer size

def main():
	# Create a TCP Server socket
	srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Enable reuse address/port
	srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	#bufsize = srvSocket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
	#print ("Buffer size [Before]:%d" %bufsize)
	#srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 256)
	#bufsize = srvSocket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
	#print ("Buffer size [After]:%d" %bufsize)

	# Bind 	on any incoming interface with PORT, '' is any interface
	print('Starting up server on port: %s' % (PORT))
	srvSocket.bind(('', PORT))
	
	# Listen incomming connection, connection number = backlog (5)
	srvSocket.listen(backlog)
	
	# Accept the incomming connection
	print('Waiting to receive message from client')
	client, (rip, rport) = srvSocket.accept()
	
	# Receive client message, buffer size = BUF_SIZE
	client_msg = client.recv(BUF_SIZE)
	while client_msg:
		msg = "Receive messgae: " + client_msg.decode('utf-8') + ",from IP: " + str(rip) + " port: " + str(rport)
		print(msg)
		client_msg = client.recv(BUF_SIZE)
	client.close()
	# Close the TCP socket
	srvSocket.close()
# end of main

if __name__ == '__main__':
	main()

####################################################
#  Network Programming - Unit 8 Non-blocking Socket         
#  Program Name: 1-NonblockingServer.py                                      			
#  The program is a simple non-blocking TCP server.            		
#  2021.07.29                                                  									
####################################################
import socket
import time

PORT = 6666
backlog = 5
recv_buff_size = 1024			# Receive buffer size

def main():
	# Create a TCP Server socket
	srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print('Starting up server on port: %s' % (PORT))
	srvSocket.bind(('', PORT))

	# Set socket non-blocking
	srvSocket.setblocking(False)
	
	# Listen incomming connection, connection number = backlog (5)
	srvSocket.listen(backlog)
	
	loop_count1 = 0
	while True:
		print('Waiting to receive message from client')
		loop_count2 = 0
		while True:
			try:
				# Accept the incomming connection
				client, (rip, rport) = srvSocket.accept()
				break
			except BlockingIOError:
				# if no incomming connection, an exception occurs
				pass
			# do something here		
			print('.(' + str(loop_count1) + ',' + str(loop_count2) + ')')
			time.sleep(1)
			# end do something here
			loop_count2 += 1
		# end while
		
		# Receive client message, buffer size = recv_buff_size
		loop_count2 = 0
		while True:
			try:
				# Receive message
				client_msg = client.recv(recv_buff_size)
				break
			except BlockingIOError:
				# if no message, an exception occurs
				pass
			# do something here		
			print('+(' + str(loop_count1) + ',' + str(loop_count2) + ')')
			time.sleep(1)
			# end do something here
			loop_count2 += 1
		# end while

		# got message
		if client_msg:
			msg = "Counr: " + str(loop_count1) + ", Receive messgae: " + client_msg.decode('utf-8') + ",from IP: " + str(rip) + " port: " + str(rport)
			print(msg)
	
			# Send message to client
			server_reply = "Server Reply: " + str(loop_count1)
			client.send(server_reply.encode('utf-8'))
		# end if
		
		client.close()
		loop_count1 += 1
	# end while
	# Close the TCP socket
	srvSocket.close()
# end of main

if __name__ == '__main__':
	main()

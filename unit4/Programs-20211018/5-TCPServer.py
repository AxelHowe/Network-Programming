####################################################
#  Network Programming - Unit 4 Concurrent Process        
#  Program Name: 5-TCPServer.py                                      			
#  The program is a concurrent TCP server.            		
#  2021.07.13                                                   									
####################################################
import socket
import threading
import time

PORT = 6666
backlog = 5
BUF_SIZE = 1024			# Receive buffer size

class ServerThread(threading.Thread):
	def __init__(self, t_name, client_sc, rip, rport):
		super().__init__(name = t_name)
		self.client = client_sc
		self.rip = rip
		self.rport = rport
		self.start()			# Start the thread when it is created
	# end for __init__()
	
	def run(self):
		name = threading.current_thread().name
		client_msg = self.client.recv(BUF_SIZE)
		if client_msg:
			msg = name + ": Receive messgae: " + client_msg.decode('utf-8') + ",from IP: " + str(self.rip) + " port: " + str(self.rport)
			print(msg)
			# wait for 5 second
			time.sleep(5)
			server_reply = name + ": Server Reply!!"
			self.client.send(server_reply.encode('utf-8'))
		self.client.close()
		print(name, 'Thread closed')
	# end run()
# end for ServerThread

def main():
	# Create a TCP Server socket
	srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Enable reuse address/port
	srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	# Bind 	on any incoming interface with PORT, '' is any interface
	print('Starting up server on port: %s' % (PORT))
	srvSocket.bind(('', PORT))
	
	# Listen incomming connection, connection number = backlog (5)
	srvSocket.listen(backlog)
	
	# Accept the incomming connection
	for i in range(10):
		t_name = 'Thread ' + str(i)
		print('Number of threads: %d' % threading.active_count())
		print('Waiting to receive message from client')
		client, (rip, rport) = srvSocket.accept()
		print('Got connection. Create thread: %s' % t_name)
		t = ServerThread(t_name, client, rip, rport)
		#t.start()
		
	# Close the TCP socket
	srvSocket.close()
# end of main

if __name__ == '__main__':
	main()

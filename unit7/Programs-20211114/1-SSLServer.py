####################################################
#  Network Programming - Unit 7 Secure Socket         
#  Program Name: 1-SSLServer.py                                      			
#  The program is a simple SSL server.            		
#  2021.07.28                                                 									
####################################################
import socket
import ssl

PORT = 6666
backlog = 5
recv_buff_size = 1024			# Receive buffer size
SERVER_CERT = './Openssl/server.cer'
SERVER_KEY = './Openssl/server.key'

def main():
	# Create  context & Load Certificate
	ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
	ctx.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
	
	# Create a TCP Server socket
	srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Enable reuse address/port
	srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	# Bind 	on any incoming interface with PORT, '' is any interface
	print('Starting up server on port: %s' % (PORT))
	srvSocket.bind(('', PORT))
	
	# Listen incomming connection, connection number = backlog (5)
	srvSocket.listen(backlog)
	
	# Wrap socket
	sslsocket = ctx.wrap_socket(srvSocket, server_side=True)
	
	# Accept the incomming connection
	print('Waiting to receive message from client')
	client, (rip, rport) = sslsocket.accept()
	
	# Receive client message, buffer size = recv_buff_size
	client_msg = client.recv(recv_buff_size)
	if client_msg:
		msg = "Receive messgae: " + client_msg.decode('utf-8') + ",from IP: " + str(rip) + " port: " + str(rport)
		print(msg)
	
		# Send message to client
		server_reply = "Application data from server!!"
		client.send(server_reply.encode('utf-8'))
		client.close()
	# Close the TCP socket
	sslsocket.close()
	srvSocket.close()
# end of main

if __name__ == '__main__':
	main()

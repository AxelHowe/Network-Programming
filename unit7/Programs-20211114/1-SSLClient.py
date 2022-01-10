####################################################
#  Network Programming - Unit 7 Secure Socket          
#  Program Name: 1-SSLClient.py                                      			
#  The program is a simple SSL client.            		
#  2021.07.28                                                  									
####################################################
import sys
import socket
import ssl

PORT = 6666
recv_buff_size = 1024			# Receive buffer size

def main():
	if(len(sys.argv) < 2):
		print("Usage: python3 1-SSLClient.py ServerIP")
		exit(1)

	# Get server IP
	serverIP = socket.gethostbyname(sys.argv[1])
	
	# Do not verify server Certificate
	ctx = ssl._create_unverified_context()
	
	# Create a TCP client socket
	cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Wrap socket
	#sslsocket = ctx.wrap_socket(cSocket, server_hostname=sys.argv[1])
	sslsocket = ctx.wrap_socket(cSocket)
	
	# Connect to server
	print('Connecting to %s port %s' % (serverIP, PORT))
	sslsocket.connect((serverIP, PORT))
	
	# Send message to server
	try:
		msg = "Application data from client!!"
		sslsocket.send(msg.encode('utf-8'))
	
		# Receive server reply, buffer size = recv_buff_size
		server_reply = sslsocket.recv(recv_buff_size)
		print(server_reply.decode('utf-8'))
	except socket.error as e:
		print('Socket error: %s' % str(e))
	except Exception as e:
		print('Other exception: %s' % str(e))
	finally:
		print('Closing connection.')
		# Close the SSL socket
		sslsocket.close()
		cSocket.close()

# end of main


if __name__ == '__main__':
	main()

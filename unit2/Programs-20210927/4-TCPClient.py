####################################################
#  Network Programming - Unit 2 Simple TCP Client Server Program         
#  Program Name: 4-TCPClient.py                                      			
#  The program is a simple TCP client. The program test the recv_buf size.           		
#  2021.07.13                                                   									
####################################################
import sys
import socket

PORT = 6666
BUF_SIZE = 1024			# Receive buffer size

def main():
	if(len(sys.argv) < 2):
		print("Usage: python3 4-TCPClient.py ServerIP")
		exit(1)

	# Get server IP
	serverIP = socket.gethostbyname(sys.argv[1])
	
	# Create a TCP client socket
	cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	#bufsize = cSocket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
	#print ("Buffer size [Before]:%d" %bufsize)
	#cSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 256)
	#bufsize = cSocket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
	#print ("Buffer size [After]:%d" %bufsize)
	
	# Connect to server
	print('Connecting to %s port %s' % (serverIP, PORT))
	cSocket.connect((serverIP, PORT))
	
	# Send message to server
	try:
		msg =  'abcdefghijklmnopqrstuvwxyz'
		for i in range(19):
			msg +=  'abcdefghijklmnopqrstuvwxyz'
		print('Send: %s' % msg)
		cSocket.send(msg.encode('utf-8'))
	except socket.error as e:
		print('Socket error: %s' % str(e))
	except Exception as e:
		print('Other exception: %s' % str(e))
	finally:
		print('Closing connection.')
		# Close the TCP socket
		cSocket.close()

# end of main


if __name__ == '__main__':
	main()

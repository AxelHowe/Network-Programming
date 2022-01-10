####################################################
#  Network Programming - Unit 9 Multicast          
#  Program Name: 1-MulticastReceiver.py                                      			
#  The program is a simple multicast receiver.            		
#  2021.08.02                                               									
####################################################
import sys
import socket
import struct

MULTICAST_GROUP1 = '225.3.2.1'
MULTICAST_GROUP2 = '225.6.7.8'
PORT = 6666
backlog = 5
BUFF_SIZE = 1024			# Buffer size

def JoinGroup(s, group_addr, flag):	# flag = True (join) / False (leave)
	# Join the multicast group, a socket can joun multiple multicast group
	# Join the multicast group by using setsockopt() to change the IP_ADD_MEMBERSHIP option
	# Leave the multicast group by using setsockopt() to change the IP_DROP_MEMBERSHIP option
	#Convert an IPv4 address from dotted-quad string format to 32-bit packed binary format, as a bytes object four characters in length.
	group = socket.inet_aton(group_addr)
	mreq = struct.pack('4sL', group, socket.INADDR_ANY)
	if flag:
		cmd = socket.IP_ADD_MEMBERSHIP
	else:
		cmd = socket.IP_DROP_MEMBERSHIP
		
	s.setsockopt(socket.IPPROTO_IP, cmd, mreq)
# end of JoinGroup

def main():
	# Create a UDP socket
	recvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	recvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# Bind 	on any incoming interface with PORT, '' is any interface
	recvSocket.bind(('', PORT))
	
	# Join the multicast group, a socket can joun multiple multicast group
	JoinGroup(recvSocket, MULTICAST_GROUP1, True)
	print('Listening on multicast group (%s, %d)' % (MULTICAST_GROUP1, PORT))
	JoinGroup(recvSocket, MULTICAST_GROUP2, True)
	print('Listening on multicast group (%s, %d)' % (MULTICAST_GROUP2, PORT))
	
	# Receive message
	for i in range(5):
		print('Waiting to receive message...')
		data, (rip, rport) = recvSocket.recvfrom(BUFF_SIZE)
		
		msg = "Receive messgae: " + data.decode('utf-8') + ",from IP: " + str(rip) + " port: " + str(rport)
		print(msg)
		
		reply = 'Message received'
		recvSocket.sendto(reply.encode('utf-8'), (rip, rport))		# Unicast
		
		if(i == 2):
			print('Leave multicast group ' + str(MULTICAST_GROUP2))
			JoinGroup(recvSocket, MULTICAST_GROUP2, False)
	
	# Leave multicast group
	print('Leave multicast group ' + str(MULTICAST_GROUP1))
	JoinGroup(recvSocket, MULTICAST_GROUP1, False)

	print('Waiting to receive message...')
	data, (rip, rport) = recvSocket.recvfrom(BUFF_SIZE)
	msg = "Receive messgae: " + data.decode('utf-8') + ",from IP: " + str(rip) + " port: " + str(rport)
	print(msg)

	# Close connection	
	recvSocket.close()
# end of main

if __name__ == '__main__':
	main()

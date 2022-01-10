####################################################
#  Network Programming - Unit 9 Multicast
#  Program Name: 1-MulticastSender.py
#  The program is a simple multicast sender.
#  2021.08.02
####################################################
import sys
import socket
import struct
import time
MULTICAST_GROUP1 = '225.3.2.1'
PORT = 6666
backlog = 5
BUFF_SIZE = 1024			# Buffer size


def JoinGroup(s, group_addr, flag):  # flag = True (join) / False (leave)
    # Join the multicast group, a socket can joun multiple multicast group
    # Join the multicast group by using setsockopt() to change the IP_ADD_MEMBERSHIP option
    # Leave the multicast group by using setsockopt() to change the IP_DROP_MEMBERSHIP option
    # Convert an IPv4 address from dotted-quad string format to 32-bit packed binary format, as a bytes object four characters in length.
    group = socket.inet_aton(group_addr)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    if flag:
        cmd = socket.IP_ADD_MEMBERSHIP
    else:
        cmd = socket.IP_DROP_MEMBERSHIP

    s.setsockopt(socket.IPPROTO_IP, cmd, mreq)
# end of JoinGroup


def main():
    global MULTICAST_GROUP
    # Create a UDP socket
    recvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind 	on any incoming interface with PORT, '' is any interface
    recvSocket.bind(('', PORT))

    # Join the multicast group, a socket can joun multiple multicast group
    JoinGroup(recvSocket, MULTICAST_GROUP1, True)
    print('Listening on multicast group (%s, %d)' % (MULTICAST_GROUP1, PORT))

    # Configure a time-to-live value (TTL) for the messages.
    #ttl = struct.pack('b', 1)
    #recvSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    print('============')
    print(recvSocket.getsockname())
    # Send message
    message = 'Hello!!'
    try:
        print('Waiting to receive message...')
        data, (rip, rport) = recvSocket.recvfrom(BUFF_SIZE)
        print('-----------------')
        print((rip, rport))
        # Send data to the multicast group
        print('sending "%s"' % message)
        sent = recvSocket.sendto(message.encode('utf-8'), (rip, rport))

        message = 1
        while True:
            print('sending "%s"' % str(message))
            sent = recvSocket.sendto(str(message).encode('utf-8'), (rip, rport))
            message += 1
            time.sleep(2)
    finally:
        print('Closing socket')
        recvSocket.close()
# end of main


if __name__ == '__main__':
    main()

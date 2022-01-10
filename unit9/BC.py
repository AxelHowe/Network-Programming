####################################################
#  Network Programming - Unit 9 Multicast
#  Program Name: 1-MulticastSender.py
#  The program is a simple multicast sender.
#  2021.08.02
####################################################
import sys
import socket
import struct

MULTICAST_GROUP = '225.6.7.8'
PORT = 6666
backlog = 5
BUF_SIZE = 1024			# Buffer size


def main():
    global MULTICAST_GROUP

    if(len(sys.argv) < 1):
        print("Usage: python3 1-MulticastSender.py group_addr")
        exit(1)

    if(len(sys.argv) > 1):
        MULTICAST_GROUP = sys.argv[1]

    # create TCP
    serverIP = '127.0.0.1'
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Connecting to %s port %s' % (serverIP, PORT))
    cSocket.connect((serverIP, PORT))
    print(' Connecting to BR')

    group = (MULTICAST_GROUP, 8888)
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely when trying to receive data.
    #sock.settimeout(0.2)

    # Configure a time-to-live value (TTL) for the messages.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    # Send message
    message = 'Hello!!'
    try:
        while True:
            message = cSocket.recv(BUF_SIZE)
            message = message.decode('utf-8')
            print('receive and send: ' + message)
            print('send: ' + message)
            sent = sock.sendto(message.encode('utf-8'), group)
    finally:
        print('Closing socket')
        sock.close()
# end of main


if __name__ == '__main__':
    main()

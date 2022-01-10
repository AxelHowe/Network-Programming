####################################################
#  Network Programming - Unit 9 Multicast
#  Program Name: 1-MulticastSender.py
#  The program is a simple multicast sender.
#  2021.08.02
####################################################
import sys
import socket
import struct

MULTICAST_GROUP = '225.3.2.1'
PORT = 6666
backlog = 5
BUFF_SIZE = 1024			# Buffer size


def main():
    global MULTICAST_GROUP

    if(len(sys.argv) < 1):
        print("Usage: python3 1-MulticastSender.py group_addr")
        exit(1)

    if(len(sys.argv) > 1):
        MULTICAST_GROUP = sys.argv[1]

    group = (MULTICAST_GROUP, PORT)
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely when trying to receive data.
    #sock.settimeout(0.2)

    # 建立 TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Starting up server on port: %s' % (PORT))
    server.bind(('', PORT))
    server.listen(backlog)
    print('Waiting to receive message from client')
    client, (rip, rport) = server.accept()

    # Configure a time-to-live value (TTL) for the messages.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    # Send message
    message = 'Hello!!'
    # Send data to the multicast group
    print('sending "%s"' % message)
    sent = sock.sendto(message.encode('utf-8'), group)
    try:
        while True:
            data, (rip, rport) = sock.recvfrom(BUFF_SIZE)
            print('Received "%s" from %s:%s' %
                (data.decode('utf-8'), str(rip), str(rport)))
            client.send(data)
        
            
    finally:
        print('Closing socket')
        sock.close()
# end of main


if __name__ == '__main__':
    main()

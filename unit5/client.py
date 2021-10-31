####################################################
#  Network Programming - Unit 5  User Datagram Protocol
#  Program Name: 2-UDPClient.py
#  This program sends 100 UDP messages.
#  2021.07.15
####################################################
import sys
import socket
import struct
import binascii
import time

PORT = 8888
BUF_Size = 1024


def main():
    if(len(sys.argv) < 2):
        print("Usage: python3 1-UDPClient.py ServerIP\n")
        exit(1)

    # Get server IP
    serverIP = socket.gethostbyname(sys.argv[1])

    # Create a UDP client socket
    dgramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s = struct.Struct('!' + 'I 15s')			# !: network orger

    num = int(input('num:'))
    # Send 100 message
    while num > 0:
        msg = 'send The %3d message' % num
        record = (num, msg.encode('utf-8'))
        packed_data = s.pack(*record)
        print(msg)
        dgramSocket.sendto(packed_data, (serverIP, PORT))

        while(1):
            try:
                dgramSocket.settimeout(0.01)
                recv_data, (rip, rport) = dgramSocket.recvfrom(BUF_Size)
                unpacked_data = s.unpack(recv_data)
                n = unpacked_data[0]
                print('Receive  message: (%s) from %s:%s' %
                      (n, str(rip), str(rport)))
                break
            except socket.timeout:
                dgramSocket.sendto(packed_data, (serverIP, PORT))
                print(msg)
        unpacked_data = s.unpack(recv_data)
        num = unpacked_data[0]

    # Close the UDP socket
    dgramSocket.close()
# end of main


if __name__ == '__main__':
    main()

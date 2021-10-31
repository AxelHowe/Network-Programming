####################################################
#  Network Programming - Unit 5  User Datagram Protocol
#  Program Name: 4-SAWServer.py
#  This program builds a server based on SAWSocket.
#  2021.07.21
####################################################
import SAWSocket
import sys
PORT = 8888
BUF_Size = 1024


def main():
    if(len(sys.argv) < 2):
        print("Usage: python3 SAWserver.py Sliding_windows\n")
        exit(1)
    if int(sys.argv[1]) < 1:
        print("Sliding_windows must be > 0\n")
        exit(1)
    w = int(sys.argv[1])
    # Create a SAWSocket Server
    server = SAWSocket.SAWSocket(8888)		# Listen on port 8888
    server.accept()

    while(1):
        import time
        time.sleep(1)

    for i in range(10):
        msg = server.receive()
        print('Receive message: ' + msg.decode('utf-8'))

    server.close()
# end of main


if __name__ == '__main__':
    main()

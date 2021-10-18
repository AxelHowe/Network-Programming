import sys
import socket
import struct
import binascii

PORT = 6666
BUF_SIZE = 1024


def main():
    if(len(sys.argv) < 2):
        print("Usage: python3 client.py ServerIP")
        exit(1)
    print('D0886096 蘇家弘')
    x = input('Input a integer: ')
    val = int(x)
    if val < 0:
        print('請輸入 >= 0 的整數')
        exit(1)
    record = val
    s = struct.Struct('!' + 'i')

    packed_data = s.pack(record)

    serverIP = socket.gethostbyname(sys.argv[1])

    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Connecting to %s port %s' % (serverIP, PORT))
    cSocket.connect((serverIP, PORT))

    def send_message(Socket, record, packed_data):
        try:
            print('Send給Server:  %s' % record)
            Socket.send(packed_data)
        except socket.error as e:
            print('Socket error: %s' % str(e))
        except Exception as e:
            print('Other exception: %s' % str(e))

    send_message(cSocket, record, packed_data)
    while(1):
        server_reply = cSocket.recv(BUF_SIZE)
        if len(server_reply) == 0:
            print('------server close-------')
            break
        unpacked_data = s.unpack(server_reply)
        print('從Server收到: ', unpacked_data[0])
        if unpacked_data[0] == 0:
            break
        record = int(unpacked_data[0]) - 1
        packed_data = s.pack(record)
        send_message(cSocket, record, packed_data)

    print('--------- close ----------')
    cSocket.close()


if __name__ == '__main__':
    main()

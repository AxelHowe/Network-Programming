####################################################
#  Network Programming - Unit 7 Secure Socket
#  Program Name: 1-SSLClient.py
#  The program is a simple SSL client.
#  2021.07.28
####################################################
import sys
import socket
import ssl
import struct

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
    x = input('Input a integer: ')
    val = int(x)
    if val < 0:
        print('請輸入 >= 0 的整數')
        exit(1)
    record = val
    s = struct.Struct('!' + 'i')
    packed_data = s.pack(record)
    # Send message to server

    def send_message(Socket, record, packed_data):
        try:
            print('Send給Server:  %s' % record)
            Socket.send(packed_data)
        except socket.error as e:
            print('Socket error: %s' % str(e))
        except Exception as e:
            print('Other exception: %s' % str(e))

    
    
    try:
        send_message(sslsocket, record, packed_data)

        while(1):
            server_reply = sslsocket.recv(recv_buff_size)
            if len(server_reply) == 0:
                print('------server close-------')
                break
            unpacked_data = s.unpack(server_reply)
            print('從Server收到: ', unpacked_data[0])
            if unpacked_data[0] == 0:
                break
            record = int(unpacked_data[0]) - 1
            packed_data = s.pack(record)
            send_message(sslsocket, record, packed_data)
    except socket.error as e:
        print('Socket error: %s' % str(e))
    except Exception as e:
        print('Other exception: %s' % str(e))
    finally:
        print('Closing connection.')
        # Close the SSL socket
        print('--------- close ----------')
        sslsocket.close()
        cSocket.close()

# end of main


if __name__ == '__main__':
    main()

####################################################
#  Network Programming - Unit 7 Secure Socket
#  Program Name: 1-SSLServer.py
#  The program is a simple SSL server.
#  2021.07.28
####################################################
import socket
import ssl
import struct

PORT = 6666
backlog = 5
recv_buff_size = 1024			# Receive buffer size
SERVER_CERT = './Openssl/server.cer'
SERVER_KEY = './Openssl/server.key'


def main():
    # Create  context & Load Certificate
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)

    # Create a TCP Server socket
    srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enable reuse address/port
    srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind 	on any incoming interface with PORT, '' is any interface
    print('Starting up server on port: %s' % (PORT))
    srvSocket.bind(('', PORT))

    # Listen incomming connection, connection number = backlog (5)
    srvSocket.listen(backlog)

    # Wrap socket
    sslsocket = ctx.wrap_socket(srvSocket, server_side=True)

    # Accept the incomming connection
    print('Waiting to receive message from client')
    client, (rip, rport) = sslsocket.accept()

    def send_message(Socket, record, packed_data):
        
        try:
            print('Send給Client:  %s' % record)
            Socket.send(packed_data)
        except socket.error as e:
            print('Socket error: %s' % str(e))
        except Exception as e:
            print('Other exception: %s' % str(e))

    while True:
        client_msg = client.recv(recv_buff_size)
        if len(client_msg) == 0:
            print('------client close-------')
            break
        s = struct.Struct('!' + 'i')
        unpacked_data = s.unpack(client_msg)
        print('從Client收到: ', unpacked_data[0])
        if unpacked_data[0] == 0:
            break
        server_reply = int(unpacked_data[0]) - 1
        packed_data = s.pack(server_reply)
        send_message(client, server_reply, packed_data)
    

    # Close the TCP socket
    print('--------- close ----------')
    sslsocket.close()
    srvSocket.close()
# end of main


if __name__ == '__main__':
    main()



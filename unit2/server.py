import socket
import struct

PORT = 6666
backlog = 5
BUF_SIZE = 1024


def main():
    print('D0886096 蘇家弘')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print('Starting up server on port: %s' % (PORT))
    server.bind(('', PORT))

    server.listen(backlog)

    print('Waiting to receive message from client')
    client, (rip, rport) = server.accept()

    msg = "Receive messgae from IP: " + str(rip) + " port: " + str(rport)
    print(msg)

    def send_message(Socket, record, packed_data):
        try:
            print('Send給Client:  %s' % record)
            Socket.send(packed_data)
        except socket.error as e:
            print('Socket error: %s' % str(e))
        except Exception as e:
            print('Other exception: %s' % str(e))

    while True:
        client_msg = client.recv(BUF_SIZE)
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
    print('--------- close ----------')
    client.close()
    server.close()


if __name__ == '__main__':
    main()

####################################################
#  Network Programming - Unit 8 Non-blocking Socket
#  Program Name: 2-MultiPortServer.py
#  The program is a simple non-blocking TCP server.
#  2021.08.02
####################################################
import sys
import socket
import select
import queue

BUF_SIZE = 1024


def main():
    if(len(sys.argv) < 2):
        print("Usage python3 2-MultiPortServer.py port1 port2 ...")
        exit(1)

    inputs = []
    srv_list = []
    outputs = []
    q = queue.Queue(maxsize=5)

    # Create sockets
    for i in range(1, len(sys.argv)):
        port = int(sys.argv[i])
        # Creat a TCP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', port))

        # Set socket non blocking
        server.setblocking(False)
        server.listen(5)

        # Add to list
        inputs.append(server)
        srv_list.append(server)
        print("Listening on port " + str(port))

    print("Waiting incomming connection ...")

    while True:
        #print('==========')
        #print(inputs)
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        #print(readable)
        for s in readable:
            if s in srv_list:		# new connection
                # Accept the incomming connection
                connection, (rip, rport) = s.accept()
                # Set the connection non blocking
                connection.setblocking(False)
                # Add connection to inputs (listen message on the connection)
                inputs.append(connection)
                laddr = connection.getsockname()
                msg = "Accept connection on port: %d from (%s, %d)" % (
                    laddr[1], str(rip), rport)
                print(msg)
            else:		# receive data
                #print('123')
                #print(s.getpeername())
                #print(s.getsockname()[1])
                raddr = s.getpeername()
                laddr = s.getsockname()
                if laddr[1] == 8880:
                
                    data = s.recv(BUF_SIZE)
                    if q.full():
                        server_reply = "Error queue is full"
                        s.send(server_reply.encode('utf-8'))
                    elif data:
                        
                        msg = "Receive messgae: " + \
                            data.decode('utf-8') + " on :" + str(laddr) + " from : " + str(raddr)
                        print(msg)
                        q.put(data.decode('utf-8'))
                        print(q.qsize())
                        print('OK')
                        server_reply = "OK"
                        s.send(server_reply.encode('utf-8'))
                    # Close connection
                    print("Close connection from: ", raddr)
                    inputs.remove(s)
                    s.close()
                    
                elif laddr[1] == 8881:
                    # Send message to client
                    # server_reply = "Server Reply!!"
                    if not q.empty():
                        data = s.recv(BUF_SIZE)
                        print(q.qsize())
                        #print('send1111')
                        server_reply = q.get()
                        #print('send1111')
                        s.send(server_reply.encode('utf-8'))
                        #print('send1111')
                        # Close connection
                        print("Close connection from: ", raddr)
                        inputs.remove(s)
                        s.close()
                
                
                
        # end for readable

        for s in exceptional:
            print("Close : ", s)
            inputs.remove(s)
            s.close()
        # end for exceptionsl
    # end for while True
# end of main()


if __name__ == '__main__':
    main()

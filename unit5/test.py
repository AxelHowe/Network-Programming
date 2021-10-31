import time
print(time.sleep(0.01))


try:
    dgramSocket.settimeout(1)
    recv_data, (rip, rport) = dgramSocket.recvfrom(BUF_Size)
except socket.timeout:
    print('123123123')

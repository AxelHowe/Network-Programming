####################################################
#  Network Programming - Unit 3 Application based on TCP         
#  Program Name: pop3client.py                                      			
#  The program is a simple POP3 client.            		
#  2021.08.03                                                   									
####################################################
import sys
import socket
from getpass import getpass
import base64
PORT = 110
BUFF_SIZE = 1024			# Receive buffer size

def ParseMessage(msg):
	line = []
	newstring = ''
	for i in range(len(msg)):
		if(msg[i] == '\n'):
			line.append(newstring)
			newstring = ''
		else:
			newstring += msg[i]
	return line
# end ParseMessage

def list_mail(Socket):
	# List [Method 1]
	cmd = 'LIST\r\n'								# don't forget "\r\n"\
	Socket.send(cmd.encode('utf-8'))
	reply = Socket.recv(BUFF_SIZE).decode('utf-8')
	print('Receive message: %s' % reply)
	if(reply[0] != '+'):
		exit(1)
		#break
	# Count mails
	line = ParseMessage(reply)
	num = len(line) - 2
	print('Mailbox has %d mails\n' % num)
	'''
	# List [Method 2]
	cmd = 'LIST\r\n'								# don't forget "\r\n"\
	Socket.send(cmd.encode('utf-8'))
	reply = Socket.recv(BUFF_SIZE).decode('utf-8')
	print('Receive message: %s' % reply)
	if(reply[0] != '+'):
		exit(1)
		#break
	# Count mails
	tokens = reply.split(' ')
	print('Mailbox has %d mails' % int(tokens[1]))
	'''

def delete_mail(Socket):
	
	x = input('要刪除第幾封信：')
	cmd = f'DELE {x}\r\n'								# don't forget "\r\n"\
	Socket.send(cmd.encode('utf-8'))
	reply = Socket.recv(BUFF_SIZE).decode('utf-8')
	print('Receive message: %s' % reply)
	if(reply[0] != '+'):
		exit(1)
		#break

def list_mail_header(Socket):
	cmd = 'LIST\r\n'								# don't forget "\r\n"\
	Socket.send(cmd.encode('utf-8'))
	reply = Socket.recv(BUFF_SIZE).decode('utf-8')
	
	if(reply[0] != '+'):
		exit(1)
		#break
	
	line = ParseMessage(reply)
	num = len(line) - 2
	

	for i in range(1, num+1):
		cmd = f'RETR {i}\r\n'
		Socket.send(cmd.encode('utf-8'))
		reply = Socket.recv(BUFF_SIZE).decode('utf-8')
		
		if(reply[0] != '+'):
			exit(1)
		line = ParseMessage(reply)
		line[14]
		print('\n')
		print('===================================')
		print('\n')
		print(f'mail {i}')
		print(line[6])
		print(line[7])
		print(line[8])
		print(line[9])
		print('\n')
		#print('===================================')

def list_mail_body(Socket):
	x = input('要讀取第幾封信：')
	cmd = f'RETR {x}\r\n'
	Socket.send(cmd.encode('utf-8'))
	reply = Socket.recv(BUFF_SIZE).decode('utf-8')
	#print('Receive message: %s' % reply)
	if(reply[0] != '+'):
		exit(1)
		#break
	line = ParseMessage(reply)
	tokens = line[15].split(' ')
	#print(tokens)
	body_line = int(tokens[1]) 
	for i in range(17, 17 + body_line + 1):
		print(line[i])

def quit(Socket):
	cmd = 'QUIT\r\n'								# don't forget "\r\n"\
	Socket.send(cmd.encode('utf-8'))
	print('Closing connection.')
	Socket.close()
	exit(1)	


def main():
	print('D0886096 蘇家弘')
	if(len(sys.argv) < 2):
		print("Usage: python3 pop3client.py ServerIP")
		exit(1)

	# Get server IP
	serverIP = socket.gethostbyname(sys.argv[1])
	
	# Get username & password
	name = input('Username: ')
	password = getpass('Password: ') 
	#name = 'iecs09'	
	#password ='6X6ZQ4WG'

	# Create a TCP client socket
	cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print('Connecting to %s port %s' % (serverIP, PORT))
	cSocket.connect((serverIP, PORT))
	try:
		# receive server greeting message
		reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
		print('Receive message: %s' % reply)
		if(reply[0] != '+'):
			exit(1)
			#break
			
		# Username
		cmd = 'USER ' + name + '\r\n'			# don't forget "\r\n"
		cSocket.send(cmd.encode('utf-8'))
		reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
		print('Receive message: %s' % reply)
		if(reply[0] != '+'):
			exit(1)
			#break

		# Password
		cmd = 'PASS ' + password + '\r\n'	# don't forget "\r\n"\
		cSocket.send(cmd.encode('utf-8'))
		reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
		print('Receive message: %s' % reply)
		if(reply[0] != '+'):
			#break
			exit(1)
	except socket.error as e:
		print('Socket error: %s' % str(e))
	except Exception as e:
		print('Other exception: %s' % str(e))

	
	while True:
		print('\n\n')
		print('|===============|')
		print('|1. show        |')
		print('|2. delete      |')
		print('|3. list header |')
		print('|4. list body   |')
		print('|5. quit        |')
		print('|===============|')
		select = input('select:')
		if select == '1':
			list_mail(cSocket)
		elif select == '2':
			delete_mail(cSocket)
		elif select == '3':
			list_mail_header(cSocket)
		elif select == '4':
			list_mail_body(cSocket)
		elif select == '5':
			quit(cSocket)
		else:
			print('錯誤輸入')
			continue
# end of main


if __name__ == '__main__':
	main()

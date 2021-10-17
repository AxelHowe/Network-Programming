####################################################
#  Network Programming - Unit 2 Simple Client Server Program         
#  Program Name: 2-remote_addr.py                                      			
#  The program gets IP address of remote host.            		
#  2021.07.13                                                   									
####################################################
import sys
import socket

def machine_info():
	host_name = socket.gethostname()
	ip_addr = socket.gethostbyname(host_name)
	return host_name, ip_addr
# end of machine_info()

def main():
	if(len(sys.argv) < 2):		# no argument
		print('Usage: python3 2-remote_addr.py host_name\n')
	else:
		try:
			ipaddr = socket.gethostbyname(sys.argv[1])
			print('IP address of %s: %s' %(sys.argv[1], ipaddr))
		except socket.error as err_msg:
			print('%s: %s' %(sys.argv[1], err_msg))
# end of mani()

if __name__ == '__main__':
	main()
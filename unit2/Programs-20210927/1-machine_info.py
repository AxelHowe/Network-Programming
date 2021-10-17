####################################################
#  Network Programming - Unit 2 Simple Client Server Program         
#  Program Name: 1-machine_info.py                                      			
#  The program gets machine name and IP address.            		
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
		host, ipaddr = machine_info()
		print('Host name: %s' % (host))
		print('IP address: %s' % (ipaddr))
	else:
		ipaddr = socket.gethostbyname(sys.argv[1])
		print('IP address of %s: %s' %(sys.argv[1], ipaddr))
# end of mani()

if __name__ == '__main__':
	main()
####################################################
#  Network Programming - Unit 4 Concurrent Process         
#  Program Name: 3-lock.py                                      			
#  The program demos the Lock primitive.           		
#  2021.07.14                                                   									
####################################################
import threading
import time

EnableCS=False

shared_variable = 0
if(EnableCS):
	lock = threading.Lock()

def modify_value(val):
	global	shared_variable
	shared_variable += val
	shared_variable -= val
# end for modify_value

def my_thread(val):
	print('Thread %s is runnung...' % threading.current_thread().name)
	if(EnableCS):
		for i in range(1000000):
			lock.acquire()
			try:
				modify_value(val)
			finally:
				lock.release()
	else:
		for i in range(1000000):
			modify_value(val)
	print('Thread %s finish' % threading.current_thread().name)
# end for my_thread()

def main():
	global	shared_variable
	print('The value of shared variable: %d' % shared_variable)
	t1 = threading.Thread(target=my_thread, args=(3,), name='T1')
	t2 = threading.Thread(target=my_thread, args=(5,), name='T2')
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	print('The value of shared variable: %d' % shared_variable)
	
# end for main()
if __name__ == '__main__':
	main()
####################################################
#  Network Programming - Unit 4 Concurrent Process         
#  Program Name: 1-thread.py                                      			
#  The program create a thread.            		
#  2021.07.14                                                   									
####################################################
import threading
import time

def loop(n):
	name = threading.current_thread().name
	print('Thread %s is runnung...' % name)
	for i in range(n):
		print(name, i)
		time.sleep(1)
# end for loop()

def main():
	print('thread %s is running...' % threading.current_thread().name)
	t1 = threading.Thread(target=loop, args=(10,), name='Loop1')
	t2 = threading.Thread(target=loop, args=(15,), name='Loop2')
	print('Number of threads: %d' % threading.active_count())
	t1.start()
	t2.start()
	print('Number of threads: %d' % threading.active_count())
	print('thread %s ended.' % threading.current_thread().name)
	
# end for main()
if __name__ == '__main__':
	main()
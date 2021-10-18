####################################################
#  Network Programming - Unit 4 Concurrent Process         
#  Program Name: 2-object_thread.py                                      			
#  The program create a thread class.            		
#  2021.07.14                                                   									
####################################################
import threading
import time

class LoopThread(threading.Thread):			# Inherit threading.Threas class
	def __init__(self, t_name, num):
		super().__init__(name=t_name)
		self.num = num
	# end for __init__()
	
	def run(self):
		name = threading.current_thread().name
		print('Thread %s is runnung...' % name)
		for i in range(self.num):
			print(name, i)
			time.sleep(1)
	#end for run()		
# end for class

def main():
	print('thread %s is running...' % threading.current_thread().name)
	t1 = LoopThread('Loop1', 10)
	t2 = LoopThread('Loop2', 15)

	print('Number of threads: %d' % threading.active_count())
	t1.start()
	t2.start()
	print('Number of threads: %d' % threading.active_count())
	print('thread %s ended.' % threading.current_thread().name)
	
# end for main()
if __name__ == '__main__':
	main()
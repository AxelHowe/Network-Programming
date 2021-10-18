####################################################
#  Network Programming - Unit 4 Concurrent Process         
#  Program Name: 4-sync1.py                                      			
#  The program demos wait() and notify() primitive.           		
#  2021.07.14                                                   									
####################################################
import threading
import time

class Resource:
	def __init__(self):
		self.value = 0
		self.lock = threading.Lock()
	# end __init__()
	
	def Create(self):
		print('Creating ........')
		time.sleep(3)
		self.lock.acquire()
		try:
			self.value += 1
		finally:
			self.lock.release()
		print('Creat one.')
	# end for Create()
	
	def Get(self):
		result = False
		self.lock.acquire()
		try:
			if(self.value > 0):
				self.value -= 1
				result = True
		finally:
			self.lock.release()
		return result
	# end for Get()
# end for class Resource

R = Resource()

class Producer(threading.Thread):
	def __init__(self, condition, num):
		super().__init__(name='Producer')
		self.condition = condition
		self.num = num
	# end for __init__()
	
	def run(self):
		global R
		name = threading.current_thread().name
		print('Thread %s is runnung...' % name)
		for i in range(self.num):
			R.Create()
			with self.condition:
				self.condition.notify()
	# end for run()
# end for class Producer

class Consumer(threading.Thread):
	def __init__(self, condition, t_name, num):
		super().__init__(name=t_name)
		self.condition = condition
		self.num = num
	# end for __init__()
		
	def run(self):
		global R
		name = threading.current_thread().name
		print('Thread %s is runnung...' % name)
		i = 0
		while(i < self.num):
			if(not R.Get()):
				print(name, 'Wait for resource...')
				with self.condition:
					self.condition.wait()
			else:
				print(name, 'Got resource.')
				i += 1
	# end for run()
# end for class Resource

def main():
	condition = threading.Condition()
	producer = Producer(condition, 10)
	consumer1 = Consumer(condition, 'Consumer1', 5)
	consumer2 = Consumer(condition, 'Consumer2', 5)
	producer.start()
	consumer1.start()
	consumer2.start()
# end for main()
if __name__ == '__main__':
	main()
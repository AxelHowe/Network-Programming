####################################################
#  Network Programming - Unit 6 Remote Procedure Call          
#  Program Name: 1-Calculator.py                                      			
#  This program is a simple calculator.           		
#  2021.07.21                                                 									
####################################################
import sys

class Calculate:
	def add(self, x, y):
		return x + y
		
	def sub(self, x, y):
		return x - y
		
	def mul(self, x, y):
		return x * y
		
	def div(self, x, y):
		return x / y
# end of class Calculate

def main():
	if(len(sys.argv) < 4):
		print("Usage: python3 1-Calculator.py  cmd x y (cmd: add, sub, mul, div)")
		exit(1)

	x = int(sys.argv[2])
	y = int(sys.argv[3])
	
	cal = Calculate()
	if(sys.argv[1] == 'add'):
		result = cal.add(x, y)
		print(str(x) + '+' + str(y) + '=' + str(result))
	elif(sys.argv[1] == 'sub'):
		result = cal.sub(x, y)
		print(str(x) + '-' + str(y) + '=' + str(result))
	elif(sys.argv[1] == 'mul'):
		result = cal.mul(x, y)
		print(str(x) + '*' + str(y) + '=' + str(result))
	elif(sys.argv[1] == 'div'):
		try:
			result = cal.div(x, y)
			print(str(x) + '/' + str(y) + '=' + str(result))
		except:
			print('Divide by zero')
	else:
			print('Usage: python3 1-Calculator.py  cmd x y (cmd: add, sub, mul, div)')
	
# end of main

if __name__ == '__main__':
	main()

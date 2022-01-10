####################################################
#  Network Programming - Unit 6 Remote Procedure Call          
#  Program Name: 7-RESTClient.py                                      			
#  This program is a simple REST API client.           		
# Install requests: pip3 install requests
#  2021.08.14                                             									
####################################################
import sys
import requests
import json

def main():
	if(len(sys.argv) < 4):
		print("Usage: python3 7-RESTClient.py serverIP port cmd (cmd = all, add, update, query) ")
		exit(1)
		
	URL = 'http://' + str(sys.argv[1]) + ':' + str(sys.argv[2]) + '/companies'

	if(sys.argv[3] == 'all'):
		# Query without parameter
		response = requests.get(URL)
		print(response.status_code)
		print(response.headers)
		print(response.text)		# response.text is a text string
	elif(sys.argv[3] == 'add'):
		# Post record
		print('Add new company')
		new_comp = input('Company name: ')
		new_city = input('City of the company: ')
		new_dict = {}
		new_dict["name"] = new_comp
		new_dict["city"] = new_city
		response = requests.post(URL, json=new_dict)
		print(response.status_code)
		print(response.headers)
		print(response.text)
	elif(sys.argv[3] == 'update'):
		print('Update a record')
		new_dict = {}
		new_dict['id'] = int(input('ID: '))
		new_dict["name"] = input('Company name: ')
		new_dict["city"] = input('City of the company: ')
		response = requests.put(URL, json=new_dict)
		print(response.status_code)
		print(response.headers)
		print(response.text)		
	elif(sys.argv[3] == 'query'):
		# Query with parameter
		city = input('City of the company: ')
		my_params = {}
		my_params["city"] = city
		response = requests.get(URL, params = my_params)
		print(response.status_code)
		print(response.headers)
		json_rec = response.json()				# response.json() is json records
		print('There are %d records' % len(json_rec)) 
		for item in json_rec:
			print('ID: %d, Company Name: %s, City: %s' % (item['id'], item['name'], item['city']))
	else:
		print("Usage: python3 7-RESTClient.py serverIP port cmd (cmd = all, add, update, query) ")
# end of main

if __name__ == '__main__':
	main()

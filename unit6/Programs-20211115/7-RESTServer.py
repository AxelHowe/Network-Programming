####################################################
#  Network Programming - Unit 6 Remote Procedure Call          
#  Program Name: 7-RESTServer.py                                      			
#  This program is a simple REST API server.           		
#  Install Flask: pip3 install flask
#  2021.08.14                                             									
####################################################
from flask import Flask, json, request, jsonify

PORT = 8080
COMP_FILE = 'company.json'

COMPANIES = []

def find_next_id():
    return max(comp["id"] for comp in COMPANIES) + 1

API = Flask(__name__)

# older version of Flask
#@API.route('/companies', methods=['GET'])
#def get_companies():
#	return json.dumps(companies)
	
@API.get("/companies")
def get_companies():
	param = request.args.get('city')
	print(param)
	if(param == None):				# no parameters
		return jsonify(COMPANIES)
	else:
		RET_COMP = []
		for i in range(len(COMPANIES)):
			if(COMPANIES[i]['city'] == param):
				RET_COMP.append(COMPANIES[i])
		return jsonify(RET_COMP)
# end of get_companies()
    
@API.post("/companies")
def add_companies():
    if request.is_json:
        new = request.get_json()
        new["id"] = find_next_id()
        COMPANIES.append(new)
        with open(COMP_FILE, 'w') as wfp:
        	json.dump(COMPANIES, wfp)
        return new, 201
    else:
    	return {"error": "Request must be JSON"}, 415
# end of add_companies()

@API.put("/companies")
def update_companies():
    if request.is_json:
        new = request.get_json()
        new_id = int(new["id"]) -1			# index begin from 0
        if(new_id >= len(COMPANIES)):
        	return {"error": "ID out of  range"}, 400
        COMPANIES[new_id] = new
        with open(COMP_FILE, 'w') as wfp:
        	json.dump(COMPANIES, wfp)
        return new, 201
    else:
    	return {"error": "Request must be JSON"}, 415
# end of update_companies()

def main():
	global COMPANIES
	
	# load JSON file
	with open(COMP_FILE) as fp:
		COMPANIES = json.load(fp)
	print(COMPANIES)
	
	API.run(host='0.0.0.0', port=PORT, debug=True)	
# end of main

if __name__ == '__main__':
	main()

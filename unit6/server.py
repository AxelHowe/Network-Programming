####################################################
#  Network Programming - Unit 6 Remote Procedure Call
#  Program Name: 7-RESTServer.py
#  This program is a simple REST API server.
#  Install Flask: pip3 install flask
#  2021.08.14
####################################################
from flask import Flask, json, request, jsonify

PORT = 8080
USER_FILE = 'user.json'

USER = []

ARTICLE_FILE = 'article.json'
ARTICLE = []

REPLY_FILE = 'reply.json'
REPLY = []
dele = []

def find_next_user_id():
    if USER == []:
        return 1
    return max(user["id"] for user in USER) + 1


def find_next_article_id():
    if ARTICLE == []:
        return 1
    return max(article["id"] for article in ARTICLE) + 1


def find_next_reply_id():
    if REPLY == []:
        return 1
    return max(reply["id"] for reply in REPLY) + 1


def find_username(username):
    for user in USER:
        if user["username"] == username:
            return True


def find_article(id):
    for article in ARTICLE:
        if article["id"] == id:
            return True
    return False


API = Flask(__name__)

# older version of Flask
# @API.route('/companies', methods=['GET'])
# def get_companies():
#	return json.dumps(companies)


# @API.get("/companies")
# def get_companies():
# 	param = request.args.get('city')
# 	print(param)
# 	if(param == None):				# no parameters
# 		return jsonify(COMPANIES)
# 	else:
# 		RET_COMP = []
# 		for i in range(len(COMPANIES)):
# 			if(COMPANIES[i]['city'] == param):
# 				RET_COMP.append(COMPANIES[i])
# 		return jsonify(RET_COMP)
# end of get_companies()


@API.post("/register")
def register():
    if request.is_json:
        user = request.get_json()
        user["id"] = find_next_user_id()
        #new["username"] = find_next_id()
        #new["password"] = find_next_id()
        if find_username(user['username']):
            return {"error": "username repeat"}, 415
        USER.append(user)
        with open(USER_FILE, 'w') as wfp:
            json.dump(USER, wfp)
        return user, 201
    else:
        return {"error": "Request must be JSON"}, 415
# end of add_companies()


@API.post("/login")
def login():
    if request.is_json:
        user = request.get_json()
        for u in USER:
            if u['username'] == user['username']:
                if u['password'] == user['password']:
                    return {"success": f"user {user['username']} login success"}, 200
                else:
                    {"error": "username or password error"}, 415
        return {"error": "username or password error"}, 415
    else:
        return {"error": "Request must be JSON"}, 415


@API.post("/create")
def create():
    if request.is_json:
        article = request.get_json()
        article["id"] = find_next_article_id()
        # if not login(article['username'], article['password']):
        #    return {"error": "username or password error"}, 415
        ARTICLE.append(article)
        with open(ARTICLE_FILE, 'w') as wfp:
            json.dump(ARTICLE, wfp)
        return article, 201
    else:
        return {"error": "Request must be JSON"}, 415


@API.get("/subject")
def subject():
    SUBJECT = []
    for subject in ARTICLE:
        SUBJECT.append({'id': subject['id'], 'subject': subject['title']})
    # print(SUBJECT)
    # print(ARTICLE)
    return jsonify(SUBJECT)


@API.post("/reply")
def reply():
    if request.is_json:
        reply = request.get_json()

        # if not login(reply['username'], reply['password']):
        #    return {"error": "username or password error"}, 415

        if not find_article(reply['article_id']):
            return {"error": "article does not exist"}, 404
        reply["id"] = find_next_reply_id()

        REPLY.append(reply)
        with open(REPLY_FILE, 'w') as wfp:
            json.dump(REPLY, wfp)
        return reply, 201
    else:
        return {"error": "Request must be JSON"}, 415


@API.get("/discussion")
def discussion():
    id = int(request.args.get('id'))
    print(id)
    print(type(id))
    print('---------------------')
    discuss = []
    if not find_article(id):
        return {"error": "article does not exist"}, 404
    for subject in ARTICLE:
        if subject['id'] == id:
            discuss.append(
                {'title': subject['title'], 'username': subject['username']})
    for reply in REPLY:
        if reply['article_id'] == id:
            discuss.append(
                {'reply': reply['reply'], 'username': reply['username']})
    #print(discuss)
    # print(SUBJECT)
    # print(ARTICLE)
    return jsonify(discuss)


@API.get("/delete")
def get_delete():
    global dele
    del dele[:]
    user = request.args.get('username')
    for article in ARTICLE:
        if article['username'] == user:
            dele.append(article)
    for reply in REPLY:
        if reply['username'] == user:
            dele.append(reply)
    return jsonify(dele)

@API.post("/delete")
def post_delete():
    global dele
    index = int(request.args.get('id'))
    print(index)
    if index >= len(dele):
        return {"error": "delete id error"}, 415
    if 'title' in dele[index]:
        for reply in list(REPLY):
            print(reply)
            if reply['article_id'] == dele[index]['id']:
                REPLY.remove(reply)
                #del reply
        ARTICLE.remove(dele[index])
    else:
        REPLY.remove(dele[index])
    with open(ARTICLE_FILE, 'w') as wfp:
        json.dump(ARTICLE, wfp)
    with open(REPLY_FILE, 'w') as wfp:
        json.dump(REPLY, wfp)
    del dele[:]
    return {},201
# @API.
# @API.put("/companies")
# def update_companies():
#     if request.is_json:
#         new = request.get_json()
#         new_id = int(new["id"]) - 1			# index begin from 0
#         if(new_id >= len(COMPANIES)):
#        	    return {"error": "ID out of  range"}, 400
#         COMPANIES[new_id] = new
#         with open(COMP_FILE, 'w') as wfp:
#        	    json.dump(COMPANIES, wfp)
#         return new, 201
#     else:
#     	return {"error": "Request must be JSON"}, 415
# end of update_companies()


def main():
    global USER, ARTICLE, REPLY

    # load JSON file
    with open(USER_FILE) as fp:
        USER = json.load(fp)
    print(USER)

    with open(ARTICLE_FILE) as fp:
        ARTICLE = json.load(fp)
    print(ARTICLE)

    with open(REPLY_FILE) as fp:
        REPLY = json.load(fp)
    print(REPLY)

    API.run(host='0.0.0.0', port=PORT, debug=True)
# end of main


if __name__ == '__main__':
    main()

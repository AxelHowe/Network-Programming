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

    URL = 'http://' + str(sys.argv[1]) + ':' + str(sys.argv[2])

    if(sys.argv[3] == 'register'):
        # Query without parameter
        username = input('username: ')
        password = input('password: ')
        new_dict = {}
        new_dict["username"] = username
        new_dict["password"] = password
        response = requests.post(URL + '/register', json=new_dict)
        print(response.status_code)
        print(response.headers)
        print(response.text)		# response.text is a text string
    elif(sys.argv[3] == 'create'):
        # Post record
        print('-----login-----')
        username = input('username: ')
        password = input('password: ')
        new_dict = {}
        new_dict["username"] = username
        new_dict["password"] = password
        response = requests.post(URL + '/login', json=new_dict)
        print(response.status_code)
        print(response.headers)
        print(response.text)
        if response.status_code == 415:
            exit(-1)  # LOG
        print('Add new article')
        title = input('article title: ')
        content = input('article content: ')
        new_dict = {}
        new_dict["username"] = username
        new_dict["password"] = password
        new_dict["title"] = title
        new_dict["content"] = content
        response = requests.post(URL + '/create', json=new_dict)
        print(response.status_code)
        print(response.headers)
        print(response.text)
    elif(sys.argv[3] == 'subject'):
        response = requests.get(URL + '/subject')
        print(response.status_code)
        print(response.headers)
        # print(response.text)
        json_rec = response.json()				# response.json() is json records
        print('There are %d article' % len(json_rec))
        for item in json_rec:
            print('%d. %s' %
                  (item['id'], item['subject']))
        # for text in response.text:
        #    print(text)
        # print(type(response.text))
        # print(response.text.split(','))
    elif(sys.argv[3] == 'reply'):
        print('-----login-----')
        username = input('username: ')
        password = input('password: ')
        new_dict = {}
        new_dict["username"] = username
        new_dict["password"] = password
        response = requests.post(URL + '/login', json=new_dict)
        print(response.status_code)
        print(response.headers)
        print(response.text)
        if response.status_code == 415:
            exit(-1)  # LOG
        # =======================
        id = int(input('article id: '))
        reply = input('reply :\n')
        my_params = {}
        my_params["username"] = username
        my_params["article_id"] = id
        my_params["reply"] = reply
        response = requests.post(URL + '/reply', json=my_params)
        print(response.status_code)
        print(response.headers)
        print(response.text)
    elif(sys.argv[3] == 'discussion'):
        id = int(input('article id: '))
        params = {}
        params['id'] = id
        response = requests.get(URL + '/discussion', params=params)
        print(response.status_code)
        print(response.headers)
        # print(response.text)
        json_rec = response.json()				# response.json() is json records
        #print('There are %d article' % len(json_rec))
        print('\n====================')
        for item in json_rec:

            if 'title' in item:
                print('subject: %s. user: %s' %
                      (item['title'], item['username']))
            else:
                print('reply: %s user: %s' %
                      (item['reply'], item['username']))
            print('====================')
    elif(sys.argv[3] == 'delete'):
        print('-----login-----')
        username = input('username: ')
        password = input('password: ')
        new_dict = {}
        new_dict["username"] = username
        new_dict["password"] = password
        response = requests.post(URL + '/login', json=new_dict)
        print(response.status_code)
        print(response.headers)
        print(response.text)
        if response.status_code == 415:
            exit(-1)  # LOG
        # =======================
        response = requests.get(URL + '/delete', params=new_dict)
        print(response.status_code)
        print(response.headers)
        # print(response.text)
        json_rec = response.json()
        print(json_rec)
        index = 0
        for item in json_rec:
            print(f'{index}.: ', end="")
            if 'title' in item:
                print('subject: %s. user: %s' %
                      (item['title'], item['username']))
            else:
                print('reply: %s user: %s' %
                      (item['reply'], item['username']))
            print('====================')
            index += 1
        id = int(input('delete id: '))
        params = {}
        params["user"] = username
        params['id'] = id
        response = requests.post(URL + '/delete', params=params)
        print(response.status_code)
        print(response.headers)
        print(response.text)
    else:
        print("Usage: python3 7-RESTClient.py serverIP port cmd (cmd = all, add, update, query) ")
# end of main


if __name__ == '__main__':
    main()

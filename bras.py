import requests
import json

path = "http://bras.nju.edu.cn:8080/selfservice"

def read_config(file_path):
    with open(file_path, 'r') as f:
        content = f.read().split('\n')
        username = content[0]
        password = content[1]
    return username, password

def login(username, password):
    hd = {"Content-type": "application/json","Accept": "application/json"}
    url = path + '/login'
    user_info = {'username':username,'password':password}
    response = requests.post(url, params=user_info, headers=hd)
    result = response.json()
    reply_code = result['reply_code']
    if reply_code == 2010101:
        print 'login successfully!'
    else:
        print 'login failed: ', result['reply_msg']
    jsessionid = response.cookies._cookies['bras.nju.edu.cn']['/']['JSESSIONID'].value
    #print 'result::', result
    #print 'cookies::', response.cookies._cookies['bras.nju.edu.cn']['/']['JSESSIONID'].value
    return {'JSESSIONID' : jsessionid}

def disconnect(uid, cookie):
    hd = {"Content-type": "application/x-www-form-urlencoded","Accept": "application/json"}
    url = path + '/disconnect'
    params = {'id':uid}
    response = requests.post(url, data=params, headers=hd, cookies=cookie)
    result = response.json()
    reply_code = result['reply_code']
    if reply_code == 2030101:
        print 'disconnect successfully!'
    else:
        print 'disconnect failed: ', result['reply_msg']
    #print response.__dict__

def online(cookie):
    hd = {"Content-type": "application/json","Accept": "application/json"}
    url = path + '/online'
    response = requests.post(url, headers=hd, cookies=cookie)
    result = response.json()
    reply_code = result['reply_code']
    if reply_code == 2030101:
        print 'online successfully!'
    else:
        print 'online failed: ', result['reply_msg']
    #print result['results']['rows']
    return result['results']['rows'][0]['id']

user_info = read_config('bras_config')
cookie = login(user_info[0], user_info[1])
uid = online(cookie)
disconnect(uid, cookie)

#! /usr/bin/env python
"""API for network access management in Nanjing University"""

import requests
import json

__author__ = "Dongliang Yu, Cunxin Jia"
__license__ = "GPL"
__status__ = "development"

portal_path = "http://p.nju.edu.cn/portal/portal_io.do"
bras_path = "http://bras.nju.edu.cn:8080/selfservice"

def read_config(file_path):
    with open(file_path, 'r') as f:
        content = f.read().split('\n')
        username = content[0]
        password = content[1]
    return username, password

def connect(username, password):
    hd = {"Content-type": "application/json","Accept": "application/json"}
    url = portal_path
    data = {'action' : 'login', 'username' : username,'password' : password}
    response = requests.post(url, data=data, headers=hd)
    result = response.json()
    reply_code = result['reply_code']
    if reply_code == 101:
        print 'connect successfully!'
    else:
        print 'connect failed:', result['reply_message']

def bras_service_login(username, password):
    hd = {"Content-type": "application/json","Accept": "application/json"}
    url = bras_path + '/login'
    user_info = {'username':username,'password':password}
    response = requests.post(url, params=user_info, headers=hd)
    result = response.json()
    reply_code = result['reply_code']
    if reply_code == 2010101:
        print 'login successfully!'
    else:
        print 'login failed: ', result['reply_msg']
    jsessionid = response.cookies._cookies['bras.nju.edu.cn']['/']['JSESSIONID'].value
    return {'JSESSIONID' : jsessionid}

def disconnect(uid, cookie):
    hd = {"Content-type": "application/x-www-form-urlencoded","Accept": "application/json"}
    url = bras_path + '/disconnect'
    params = {'id':uid}
    response = requests.post(url, data=params, headers=hd, cookies=cookie)
    result = response.json()
    reply_code = result['reply_code']
    if reply_code == 2030101:
        print 'disconnect successfully!'
    else:
        print 'disconnect failed: ', result['reply_msg']

def get_online_info(cookie):
    hd = {"Content-type": "application/json","Accept": "application/json"}
    url = bras_path + '/online'
    response = requests.post(url, headers=hd, cookies=cookie)
    result = response.json()
    reply_code = result['reply_code']
    if reply_code == 2030101:
        print 'online successfully!'
    else:
        print 'online failed: ', result['reply_msg']
    return result['results']['rows'][0]['id']

if __name__ == '__main__':
    user_info = read_config('bras_config')
    #connect(user_info[0], user_info[1])
    cookie = bras_service_login(user_info[0], user_info[1])
    uid = get_online_info(cookie)
    disconnect(uid, cookie)

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

def connect(user_info):
    username = user_info[0]
    password = user_info[1]
    headers = {"Content-type" : "application/json","Accept" : "application/json"}
    url = portal_path
    data = {'action' : 'login', 'username' : username,'password' : password}
    response = requests.post(url, data=data, headers=headers)
    result = response.json()
    reply_code = result['reply_code']
    if reply_code == 101:
        print 'connect successfully!'
    else:
        print 'connect failed:', result['reply_message']

def bras_service_login(user_info):
    username = user_info[0]
    password = user_info[1]
    headers = {"Content-type" : "application/json","Accept" : "application/json"}
    url = bras_path + '/login'
    params = {'username' : username,'password' : password}
    response = requests.post(url, params=params, headers=headers)
    result = response.json()
    reply_code = result['reply_code']
    if reply_code == 2010101:
        print 'bras service login successfully.'
        jsessionid = response.cookies._cookies['bras.nju.edu.cn']['/']['JSESSIONID'].value
        return {'JSESSIONID' : jsessionid}
    else:
        print 'bras service login failed: ', result['reply_msg']
        return None

def disconnect(uid, cookie):
    hd = {"Content-type" : "application/x-www-form-urlencoded","Accept" : "application/json"}
    url = bras_path + '/disconnect'
    params = {'id' : uid}
    response = requests.post(url, data=params, headers=hd, cookies=cookie)
    result = response.json()
    reply_code = result['reply_code']
    if reply_code == 2030101:
        print 'disconnect successfully!'
    else:
        print 'disconnect failed: ', result['reply_msg']

def get_online_info(cookie):
    headers = {"Content-type" : "application/json","Accept" : "application/json"}
    url = bras_path + '/online'
    response = requests.post(url, headers=headers, cookies=cookie)
    result = response.json()
    reply_code = result['reply_code']
    if reply_code == 2030101:
        print 'get online info successfully.'
        return result['results']['rows'][0]['id']
    else:
        print 'get online info failed: ', result['reply_msg']
        return None

if __name__ == '__main__':
    """force disconnect"""
    user_info = read_config('bras_config')
    cookie = bras_service_login(user_info)
    if cookie:
        uid = get_online_info(cookie)
        if uid:
            disconnect(uid, cookie)
    """connect
    connect(user_info)
    """

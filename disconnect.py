#! /usr/bin/env python

from bras import *

def force_disconnect():
    user_info = read_config('bras_config')
    cookie = bras_service_login(user_info)
    if cookie:
        uid = get_online_info(cookie)
        if uid:
            disconnect(uid, cookie)

if __name__ == '__main__':
    force_disconnect()

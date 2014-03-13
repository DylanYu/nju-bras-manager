#! /usr/bin/env python

import sys 
import os
from bras import *

def force_disconnect():
    abspath = os.path.abspath(sys.argv[0])
    config_path = os.path.dirname(abspath) + '/bras_config'
    user_info = read_config(config_path)
    cookie = bras_service_login(user_info)
    if cookie:
        uid = get_online_info(cookie)
        if uid:
            disconnect(uid, cookie)

if __name__ == '__main__':
    force_disconnect()

#! /usr/bin/env python

import sys 
import os
from bras import *
from disconnect import *

def force_connect():
    force_disconnect()
    abspath = os.path.abspath(sys.argv[0])
    config_path = os.path.dirname(abspath) + '/bras_config'
    user_info = read_config(config_path)
    connect(user_info)

if __name__ == '__main__':
    force_connect()

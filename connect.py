#! /usr/bin/env python

from bras import *
from disconnect import *

def force_connect():
    force_disconnect()
    user_info = read_config('bras_config')
    connect(user_info)

if __name__ == '__main__':
    force_connect()

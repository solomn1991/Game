import psutil

import os
import time
import gc
import sys

def get_this_ps_memory_token():
    print(str(psutil.Process(os.getpid()).memory_info().rss/1024/1024)+" M")


class Interface(object):

    def __init__(self):
        self.space = '1'*1024*1024*50

    def print_123(self):

        print(1234)


class Room(object):

    def __init__(self):
        self.space = '1'*1024*1024*250


get_this_ps_memory_token()
inte = Interface()
get_this_ps_memory_token()
room = Room()
get_this_ps_memory_token()
inte.room = room
room.inte = inte
get_this_ps_memory_token()

inte.room.inte.room = None
room.inte = None
del room


get_this_ps_memory_token()
print(123)


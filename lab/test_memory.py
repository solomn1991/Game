import psutil

import os
import time
import gc
import sys








class Inner_object(object):

    def __init__(self,outter_object):
        self.outter_object = outter_object
        self.space = '1'*1024*1024*50


class Outter_object(object):

    def __init__(self):
        self.space = '1' * 1024 * 1024 * 10
        print(get_this_ps_memory_token())

        self.inner_object = Inner_object(self)
        print(get_this_ps_memory_token())




    def get_inner_object(self):
        return self.inner_object


def get_this_ps_memory_token():
    return str(psutil.Process(os.getpid()).memory_info().rss/1024/1024)+" M"

print("memory token:",get_this_ps_memory_token())

outter_object = Outter_object()

print("memory token:",get_this_ps_memory_token())

print('outter_object refcount:',sys.getrefcount(outter_object))
print('inner_object refcount:',sys.getrefcount(outter_object.inner_object))










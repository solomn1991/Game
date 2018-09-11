import gc
import sys
import psutil

import os
import objgraph


class OBJ():
    def __init__(self):

        self.space = '1' * 1024 * 1024 * 50

a,b = OBJ(),OBJ()
def show_detail():
    print('a refcount', sys.getrefcount(a), 'b refcount', sys.getrefcount(b),"本进程占用",str(psutil.Process(os.getpid()).memory_info().rss/1024/1024)+" M")


a.attr_b = b
a.attr_b = None

objgraph.show_backrefs(a, max_depth=5, filename = "indirect.dot")




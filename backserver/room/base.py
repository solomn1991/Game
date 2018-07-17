# coding:utf-8
# author:赵越超
import weakref

class BaseRoom(object):

    def __init__(self,*args,**kwargs):
        self.room_service = kwargs.get("room_service")
        self.room_id = kwargs.get("room_id")


    def destory(self):
        self.game.destory()
        del self.room_service.rooms[self.room_id]
        self.room_service = None #解除循环引用
    

    def enter(self):
        raise NotImplementedError


    def sit_down(self):
        raise NotImplementedError


    def ready(self):
        raise NotImplementedError


    def dissolve(self):#解散房间
        raise NotImplementedError


    def exit(self,player):
        raise NotImplementedError





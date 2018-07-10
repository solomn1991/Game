# coding:utf-8
# author:赵越超


class BaseRoom(object):

    def test(self):
        return{"hello":"world"}

    def __init__(self,*args,**kwargs):
        self.room_service = kwargs.get("room_service")
    

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




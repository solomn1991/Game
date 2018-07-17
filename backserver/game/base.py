
class base(object):

    def __init__(self,room,*args,**kwargs):

        self.room = room
        self.game_data = {}

    def get_all_game_data(self,user_info):
        return  {"msg":"获取游戏信息成功","game_data":self.game_data}

    def stand_up(self):
        pass

    def sit_down(self):
        pass

    def destory(self):
        self.room.game = None
        self.room = None #用于解除循环引用导致的不释放
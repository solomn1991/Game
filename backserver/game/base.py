class base(object):

    def __init__(self,room):

        self.room = room
        self.game_data = {}

    def get_all_game_data(self):
        return  {"msg":"获取游戏信息成功","game_data":self.game_data}

    def stand_up(self):
        pass

    def sit_down(self):
        pass
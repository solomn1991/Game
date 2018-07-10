from .base import BaseRoom
from User.Player import Player
from autobahn.wamp.types import PublishOptions


class FlexSeatRoom(BaseRoom):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.init_data(*args,**kwargs)

    def init_data(self,*args,**kwargs):
        self.room_id = kwargs.get("room_id")
        self.game = None
        self.available_seat_num = kwargs.get("kwargs") or 6
        self.room_channel = self.room_service.server_ip+".room."+str(self.room_id)


        self.all_player = {}
        self.seat_player_map = {}





    async def enter(self,user_info):
        #重复玩家判断
        result = {}
        if self.game:
            result = self.game.get_all_game_data(user_info)

        res = await self.room_service.call("RelationshipService.relate_room_player",self.room_id,user_info["user_id"])

        inform = {
            "handler":"on_enter",
            "args":[]
        }
        res = self.room_service.publish(self.room_channel,
                                        inform,
                                        # options=PublishOptions(eligible_authid=["asurack"]),
                                        options=PublishOptions())

        return result


    async def sit_down(self,user_info,position):
        player = Player(user_info)

        result = {"success":True}
        self.seat_player_map[position] = player
        return result

    def stand_up(self,user_info,position):
        result = self.game.stand_up(user_info,position)





    def ready(self,position):
        if all(self.players.is_ready):
            pass



    def dissolve(self):#解散房间
        self.save_room_history()
        return True


    def exit(self,player):
        raise NotImplementedError


    def save_room_history(self):
        pass



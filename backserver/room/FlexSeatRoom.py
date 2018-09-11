from .base import BaseRoom
from User.Player import Player
from autobahn.wamp.types import PublishOptions


from game import gamenum_gametype_map



class FlexSeatRoom(BaseRoom):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.init_data(*args,**kwargs)

    def init_data(self,*args,**kwargs):

        self.game = gamenum_gametype_map[kwargs["game_num"]](self)
        self.available_seat_num = kwargs.get("kwargs") or 6
        self.room_channel = self.room_service.server_ip+".room."+str(self.room_id)
        self.game.min_num = 2


        self.all_player = {} #所有进入房间的玩家
        self.seat_player_map = {
           i+1:None for i in range(self.available_seat_num)
        }

    async def enter(self,user_info):
        result = {}
        user_id = user_info["user_id"]

        if not user_id in self.all_player:
            player = Player(user_info)
            self.all_player[user_id] = player

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

            result.update({"success":True,"msg":"正常进入房间"})

        else:
            result.update({"success":True,"msg":"已经在房间中"})


        return result

    async def sit_down(self,user_info,position):
        # 简易坐下规则
        # 限制,必须是已经进入房间的玩家(in self.all_players)
        # 关于坐下,无论游戏和非游戏时间都能坐下
        # 未坐下的玩家坐下最简单，坐下即可
        # 已坐下玩家发坐下，判断其位置与原有位置是否相同,若已坐下，则为切换位置,游戏中的玩家不能切换位置

        user_id = user_info.get("user_id")
        assert user_id in self.all_player,'请求玩家未在房间中,请求非法'

        if self.seat_player_map[position]:
            result = {"success":False,"reason":"座位上已有人了"}
        else:
            if user_id in self.seat_player_map.values():
                if self.game and self.game.is_gaming() and user_id is self.game.get_player_ids():
                    result = {"success":False,"reason":"切换位置失败,游戏正在进行中,并且玩家正处于局当中"}
                else:
                    result = {"success":True,"reason":"切换位置成功"}

            else:
                self.seat_player_map[position] = user_id
                result = {"success":True,"msg":"坐下成功"}

        return result

    def stand_up(self,user_info,position):
        user_id = user_info.get("user_id")
        assert user_id in self.seat_player_map.values(),"玩家没有坐下，无法站起"#发了这个说明前端处理存在问题
        if self.game and self.game.is_gaming() and user_id is self.game.get_player_ids():
            result = {"success": False, "reason": "站起失败,游戏正在进行中,并且玩家正处于局当中"}#理论上会发这个也是前端bug
        else:
            assert self.seat_player_map[position]==user_id,"发起请求玩家不是坐在该位子上玩家，请求非法"
            self.self.seat_player_map[position] = None
            inform = {
                "handler":"on_someone_standup",
                "args":[user_id]
            }
            res = self.room_service.publish(self.room_channel,
                                            inform,
                                            options=PublishOptions())

            result = {"success":True,"msg":"站起成功"}

        return result

    async def ready(self,user_info):
        user_id = user_info.get("user_id")
        all_sitting_players = [self.all_player[self.seat_player_map[tmp_user_id]] for tmp_user_id in self.seat_player_map if self.seat_player_map[tmp_user_id]]
        if all([sitting_player.is_ready for sitting_player in all_sitting_players]) and len(all_sitting_players)>=self.game.min_num:
            self.game.start()

        else:
            inform = {
                "handler":"on_someone_ready",
                "args":[user_id]
            }

            res = self.room_service.publish(self.room_channel,
                                            inform,
                                            options=PublishOptions(exclude_authid=[user_id]))

        result = {"success":True,"msg":"准备成功"}

        return result

    def dissolve_room(self):#解散房间
        raise NotImplementedError
        self.save_room_history()
        self.destory()
        return True

    def exit(self,user_info):

        #如果在游戏中
        raise NotImplementedError

    def save_room_history(self):
        pass



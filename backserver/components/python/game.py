# coding:utf-8
# author:赵越超

# coding:utf-8
# author:赵越超
import sys

import os
work_dir = os.getcwd()
sys.path.append(work_dir)
import config

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import RegisterOptions

from room import BaseRoom


class GameComponent(ApplicationSession):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.room_id2room = {}
        self.player_id2room_id = {}


    def onJoin(self, details):
        print("游戏服务器",config.SERVER_IP,"加入Crossbar")

        rpc_route = config.SERVER_IP+"."+"create_room"
        self.register(self.create_room,rpc_route)
        print("注册",rpc_route,"完成")

        rpc_route = config.SERVER_IP + "." + "room_operate.."
        self.register(self.room_operate, rpc_route,RegisterOptions(match="wildcard",details_arg='details'),)
        print("注册", rpc_route, "完成")


    def get_available_room_id(self):
        if not self.room_id2room:
            room_id = 0
        else:
            room_id = max(self.room_id2room)+1

        return room_id


    def create_room(self,room_type):
        print("创建房间类型",room_type)
        room_id = self.get_available_room_id()
        room = BaseRoom()
        self.room_id2room[room_id] = room
        result = {"success":True,"room_id":room_id}
        return  result


    async def room_operate(self,*args,**kwargs):

        caller_session_id = kwargs.get("details").caller

        session_info = await self.call("wamp.session.get",caller_session_id)


        pattern_url = kwargs.get("details").procedure
        print("calling",pattern_url)

        url_prefix = config.SERVER_IP+".room_operate."
        inner_operation = pattern_url.replace(url_prefix,"")

        room_id,operation_name = inner_operation.split(".")
        room_id = int(room_id)
        room = self.room_id2room[room_id]

        handler = getattr(room,operation_name)
        assert handler,"该方法不存在"

        operation_data = kwargs.get("operation_data")
        op_args = operation_data.get("args",())
        op_kwargs = operation_data.get("kwargs",{})

        result = handler(*op_args,**op_kwargs)
        return result





if __name__=="__main__":

    if len(sys.argv)==1:

        crossbar_url = "ws://127.0.0.1:8080/ws_for_server"
        realm = "game"
    else:
        crossbar_url = sys.argv[1]
        realm = sys.argv[2]

    runner = ApplicationRunner(crossbar_url,realm)
    runner.run(GameComponent)

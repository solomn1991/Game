# coding: utf-8

# 本服务用于房间的创建，及其相关的控制
# 游戏的创建，及其相关的控制

import sys
import os
import inspect

work_dir = os.getcwd()
sys.path.append(work_dir)
import config
import traceback


from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from room import FlexSeatRoom
from autobahn.wamp.types import RegisterOptions


class RoomManager(ApplicationSession):#comp
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.rooms = {}
        self.server_ip = config.SERVER_IP


    async def onJoin(self, details):
        print("Room Server",config.SERVER_IP,"加入Crossbar")

        rpc_route = config.SERVER_IP + "." + "room_operate.."
        self.register(self.room_operate, rpc_route,RegisterOptions(match="wildcard",details_arg='details'),)
        print("注册", rpc_route, "完成")
        print("Room server started")


    def get_available_room_id(self):
        if not self.rooms:
            room_id = 0
        else:
            room_id = max(self.rooms)+1

        return room_id


    def create_room(self,game_num):
        room_id = self.get_available_room_id()
        room = FlexSeatRoom(room_service=self,room_id=room_id,game_num=game_num)
        self.rooms[room_id] = room
        msg = "创建房间成功"
        result = {"success":True,"room_id":room_id,"msg":msg}
        return  result

    async def room_operate(self, *args, **kwargs):
        caller_session_id = kwargs.get("details").caller

        session_info = await self.call("wamp.session.get", caller_session_id)
        username = session_info.get("authextra",{}).get("username")
        user_id = session_info.get("authextra",{}).get("user_id")
        user_role = session_info.get("authrole")
        user_info = {user_role:username,"user_id":str(user_id)}

        pattern_url = kwargs.get("details").procedure
        print("calling", pattern_url)

        url_prefix = config.SERVER_IP + ".room_operate."
        inner_operation = pattern_url.replace(url_prefix, "")

        operation_data = kwargs.get("operation_data",{})
        op_args = operation_data.get("args", ())
        op_kwargs = operation_data.get("kwargs", {})

        op_kwargs["user_info"] = user_info


        try:
            if inner_operation=="create_room.new":
                game_num = op_kwargs.get("game_num")
                result = self.create_room(game_num=game_num)
            else:
                room_id, operation_name = inner_operation.split(".")
                room_id = int(room_id)
                if not room_id in self.rooms:
                    result = {"success":False,"reason":"房间不存在"}
                else:
                    room = self.rooms[room_id]

                    handler = getattr(room, operation_name)
                    assert handler, "该方法不存在"
                    result =  handler(*op_args, **op_kwargs)


                    if inspect.iscoroutine(result):
                        result = await result



        except Exception as e:
            print(traceback.format_exc())
            result = {"success":False,"reason":"未知异常","trace_info":traceback.format_exc()}



        return result



if __name__=="__main__":


    if len(sys.argv)==1:

        crossbar_url = "ws://127.0.0.1:8080/ws_for_server"
        realm = "game"
    else:
        crossbar_url = sys.argv[1]
        realm = sys.argv[2]

    runner = ApplicationRunner(crossbar_url, realm)
    runner.run(RoomManager)





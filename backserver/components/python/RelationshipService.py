# coding:utf-8
# author:赵越超

# 本服务的主要功能，用于管理游戏中玩家，房间的关系，以及相关的关系的增删查改
# 0 容错


import sys
import asyncio

import os
work_dir = os.getcwd()
sys.path.append(work_dir)
import config

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import PublishOptions




class RelationshipManager(ApplicationSession):#comp

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.room_id2player_ids = {}
        self.player_id2room_ids = {}

    def onJoin(self, details):
        # rpc_route = "get_availabe_room_id"
        # self.register(self.auth, rpc_route)
        self.register(self.relate_room_player,"RelationshipService.relate_room_player")
        self.register(self.release_relationship,"RelationshipService.release_relationship")
        print("Relationship server started")



    def get_player_ids_by_room_id(self,room_id):
        pass

    def get_room_ids_by_player_id(self,player_id):
        pass

    def relate_room_player(self,room_id,player_id):
        if not room_id in self.room_id2player_ids:
            self.room_id2player_ids[room_id] = set()

        self.room_id2player_ids[room_id].add(player_id)

        if not player_id in self.player_id2room_ids:
            self.player_id2room_ids[player_id] = set()
        self.player_id2room_ids[player_id].add(player_id)
        result = {"success":True,"msg":"建立房间关系成功,成功关联玩家:"+player_id+"与房间:"+str(room_id)}
        return  result

    def release_relationship(self,player_id,room_id):

        result = {"success":False,"msg":""}
        if player_id in self.player_id2room_ids and room_id in self.player_id2room_ids[player_id]:
            self.player_id2room_ids[player_id].remove(player_id)
            result["msg"] += "解除关系时玩家--房间关系成功;"
        else:
            result["msg"] += "解除关系时玩家--房间关系存在问题;"

        if room_id in self.room_id2player_ids and room_id in self.room_id2player_ids[room_id]:
            self.room_id2player_ids[room_id].remove(room_id)
            result["msg"] += "解除关系时房间--玩家关系成功;"
        else:
            result["msg"] += "解除关系时房间--玩家关系存在问题;"

        result["success"] = True

        return result





if __name__=="__main__":

    if len(sys.argv)==1:

        crossbar_url = "ws://127.0.0.1:8080/ws_for_server"
        realm = "game"
    else:
        crossbar_url = sys.argv[1]
        realm = sys.argv[2]

    runner = ApplicationRunner(crossbar_url,realm)
    runner.run(RelationshipManager)

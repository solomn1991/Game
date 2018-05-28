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

        self.room_id2room = {}
        self.player_id2room_id = {}

    def onJoin(self, details):
        # rpc_route = "get_availabe_room_id"
        # self.register(self.auth, rpc_route)
        print("Relationship server started")



    def get_player_ids_by_room_id(self,room_id):
        pass

    def get_room_ids_by_player_id(self,player_id):
        pass



if __name__=="__main__":

    if len(sys.argv)==1:

        crossbar_url = "ws://127.0.0.1:8080/ws_for_server"
        realm = "game"
    else:
        crossbar_url = sys.argv[1]
        realm = sys.argv[2]

    runner = ApplicationRunner(crossbar_url,realm)
    runner.run(RelationshipManager)

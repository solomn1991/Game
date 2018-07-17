# coding:utf-8
# author:赵越超


import asyncio
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import auth

import pprint


USER="solomn"
USER_SECRET = "123456"

class RoomGameData(object):
    def __init__(self):
        all_data = {}

        self.player_ids = []
        all_data["player_ids"] = self.player_ids

    def on_enter(self,*args):
        print(args)


room_game_data = RoomGameData()



def on_event(data):
    handler = getattr(room_game_data,data.get("handler"))
    args = data.get("args")
    res = handler(*args)
    return res


class MyComponent(ApplicationSession):


    def onConnect(self):
        self.join(self.config.realm, [u"wampcra"],USER)

    def onChallenge(self, challenge):
        key = USER_SECRET
        signature = auth.compute_wcs(key, challenge.extra['challenge'])
        return signature


    async def onJoin(self, details):
        # # listening for the corresponding message from the "backend"
        # # (any session that .publish()es to this topic).
        # def onevent(msg):
        #     print("Got event: {}".format(msg))
        # await self.subscribe(onevent, u'com.myapp.hello')

        # call a remote procedure.

        # res = await self.call('127.0.0.1.room_operate.0.test',operation_data={"args":(),"kwargs":{}})
        res = await self.call('127.0.0.1.room_operate.create_room.new',operation_data={"args":(),"kwargs":{"game_num":1}})
        print("Got result: {}".format(res))
        room_id = res.get("room_id")
        res = await self.subscribe(on_event, "127.0.0.1.room." + str(room_id))
        res = await self.call('127.0.0.1.room_operate.'+str(room_id)+".enter",operation_data={"args":(),"kwargs":{}})
        print("Got result: {}".format(res))







if __name__ == '__main__':
    runner = ApplicationRunner(
         u"ws://127.0.0.1:8080/ws_for_client",
        u"game",
    )
    runner.run(MyComponent)
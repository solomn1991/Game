# coding:utf-8
# author:赵越超


import asyncio
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import auth

import pprint


USER="solomn"
USER_SECRET = "123"


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

        res = await self.call('127.0.0.1.create_room', "chat")
        res = await self.call('127.0.0.1.room_operate.0.test',operation_data={"args":(),"kwargs":{}})
        print("Got result: {}".format(res))




if __name__ == '__main__':
    runner = ApplicationRunner(
         u"ws://127.0.0.1:8080/ws_for_client",
        u"game",
    )
    runner.run(MyComponent)
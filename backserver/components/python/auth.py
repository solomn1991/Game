# coding:utf-8
# author:赵越超
import sys
import os

work_dir = os.getcwd()
sys.path.append(work_dir)
import config

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import RegisterOptions



class AuthComponent(ApplicationSession):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)



    def onJoin(self, details):
        rpc_route = "auth"
        self.register(self.auth,rpc_route)


    def auth(self,realm, authid, details):
        print("认证",authid,"中")
        result = {
            'realm':"game",
            'role':"client",
            'secret':'123',
            'extra':{
                "user_id": 1,
                "username": "abc"
            }

        }
        return result


if __name__=="__main__":


    if len(sys.argv)==1:

        crossbar_url = "ws://127.0.0.1:8080/ws_for_server"
        realm = "game"
    else:
        crossbar_url = sys.argv[1]
        realm = sys.argv[2]

    runner = ApplicationRunner(crossbar_url, realm)
    runner.run(AuthComponent)





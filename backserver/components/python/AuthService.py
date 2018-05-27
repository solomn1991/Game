# coding:utf-8
# author:赵越超
import sys
import os

work_dir = os.getcwd()
sys.path.append(work_dir)
import config
import database
from database.models import User

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import RegisterOptions





class AuthManager(ApplicationSession):#comp
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)



    def onJoin(self, details):
        rpc_route = "auth"
        self.register(self.auth,rpc_route)
        print("Auth server finish start")


    async def auth(self,realm, authid, details):
        account = authid
        result = {}

        user = await database.db_objects.get(User,account=account)
        if user:
            print("认证",authid,"中")
            result = {
                'realm':"game",
                'role':"client",
                'secret':user.password,
                'extra':{
                    "user_id": user.id,
                    "username": user.username
                }

            }
        print("Auth result",result)
        return result



if __name__=="__main__":


    if len(sys.argv)==1:

        crossbar_url = "ws://127.0.0.1:8080/ws_for_server"
        realm = "game"
    else:
        crossbar_url = sys.argv[1]
        realm = sys.argv[2]

    runner = ApplicationRunner(crossbar_url, realm)
    runner.run(AuthManager)





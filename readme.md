技术栈

通讯方面
1.crossbar.io ==> 用于实现基本的rpc通讯

python
1.peewee ==> 用于实现数据库的orm,以实现数据固化
2.picle ==> 用于实现重启时的数据序列化存储，以便再次启动服务时，将更新前运行的数据读入
3.wamp协议的python版本，用于服务端的交互

前端js
1.cocoscreator ==> 用于实现前端游戏的前端
2.wamp的js版本，用于和crossbar交互

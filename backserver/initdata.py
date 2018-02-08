# coding:utf-8
# author:赵越超


from database import db
from database.models import *



# 1.创建表 if not exits
# 2.清理表
# 3.造数据
#todo 检验创建表是否有效

db.connect()


db.create_tables([User])
User.delete().execute()


user_infos = [
    {"account":"solomn","password":"123456","username":"逆流而上的鱼"},
    {"account":"asurack","password":"123456","username":"油泼面"},
    {"account":"pikaqiu","password":"123456","username":"皮卡丘"},
    {"account":"KFC","password":"123456","username":"肯打鸡"},
    {"account":"Franie","password":"123456","username":"小笼包"},

]


for user_info in user_infos:
    user = User(**user_info)
    user.save()


# coding:utf-8
# author:赵越超


from database import db
from database.models import *


db.connect()
db.create_tables([User])



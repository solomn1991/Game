# coding:utf-8
# author:赵越超

from peewee import *

from database import db


class User(Model):
    account = CharField()
    password = CharField()
    username = CharField()
    test = CharField(null=True)

    class Meta:
        database = db
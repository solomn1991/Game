# coding:utf-8
# author:赵越超
from peewee import SqliteDatabase

import config


db = SqliteDatabase(config.SQLITE_PATH)
# coding:utf-8
# author:赵越超
import asyncio
from peewee_async import Manager,PostgresqlDatabase


import config


loop = asyncio.get_event_loop()
db = PostgresqlDatabase(config.PG_DB_NAME,user=config.PG_DB_USER,password=config.PG_DB_PASSWORD)
db_objects = Manager(db,loop=loop)
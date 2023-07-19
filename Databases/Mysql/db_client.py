# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/5/10 14:35

from peewee_async import PooledMySQLDatabase, Manager
from peewee import Model
from Configure import cfg

# 连接池
# db_lbk = PooledMySQLDatabase(
#     cfg.MYSQL.lbk_db,
#     max_connections=500,
#     user=cfg.MYSQL.user,
#     host=cfg.MYSQL.host,
#     port=cfg.MYSQL.port,
#     password=cfg.MYSQL.password,
# )
db_cex = PooledMySQLDatabase(
    cfg.MYSQL.cex_db,
    max_connections=500,
    user=cfg.MYSQL.user,
    host=cfg.MYSQL.host,
    port=cfg.MYSQL.port,
    password=cfg.MYSQL.password,
)


# class LBKModel(Model):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__()
#         self.atomic = db_lbk.atomic_async   # 异步事物
#         self.object = Manager(db_lbk)       # 添加Manager类
#
#     class Meta:
#         database = db_lbk


class CEXModel(Model):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.atomic = db_cex.atomic_async   # 异步事物
        self.object = Manager(db_cex)       # 添加Manager类

    class Meta:
        database = db_cex


if __name__ == "__main__":
    pass

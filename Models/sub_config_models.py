# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/6/15 12:04

import sys
sys.path.append("/root/WssMiddlewareV2")

from peewee import CharField, BooleanField, DateTimeField, SQL

from Databases import CEXModel


class SubscribeConfigModel(CEXModel):

    symbol = CharField(max_length=32, help_text="币对(btc_usdt)")
    exchange = CharField(default="lbank", max_length=32, help_text="交易所")
    type = CharField(default="spot", max_length=16, help_text="类型(spot|swap)")
    status = BooleanField(default=True, help_text="是否启动订阅")
    business = CharField(default="depth", max_length=32, help_text="订阅类型(depth|kline)")
    params = CharField(default="", null=True, help_text="参数(depth: time|level kline: time|period|limit)")
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")])
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = "subscribe_config"
        indexes = (
            (("symbol", "exchange", "type", "status"), False),
        )
        mysql_engine = "InnoDB"     # 设置表的引擎为 InnoDB
        mysql_charset = "utf8mb4"   # 设置表的字符集为 utf8mb4-general-ci


if __name__ == "__main__":
    from Databases import db_cex

    tables = [
        SubscribeConfigModel,
    ]

    db_cex.drop_tables(tables)
    db_cex.create_tables(tables)

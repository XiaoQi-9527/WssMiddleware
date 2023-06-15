# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/4/6 15:11

from dataclasses import dataclass


@dataclass(frozen=True)
class Mysql:
    host: str = "127.0.0.1"
    port: int = 3306
    user: str = "root"
    password: str = "lbk369"
    max_connections: int = 500

    sys_db: str = "monitor_sys"
    lbk_db: str = "lbk_api"
    dex_db: str = "dex_db"
    cex_db: str = "cex_db"


@dataclass(frozen=True)
class Redis:
    host: str = "127.0.0.1"
    port: int = 6379
    password: str = "8y7bZzQr3"
    max_connections: int = 500


@dataclass(frozen=True)
class Config:

    MYSQL = Mysql
    REDIS = Redis

    SECRET_KEY: str = "EACex0.0"


if __name__ == '__main__':
    pass

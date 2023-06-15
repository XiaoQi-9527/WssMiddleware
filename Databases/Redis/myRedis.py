# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/3/28 16:44

from typing import Union

from ujson import loads, dumps
from redis import StrictRedis, ConnectionPool

from Configure import cfg


class MyRedis:

    def __init__(self, db: int = 0):
        self._pool = ConnectionPool(
            max_connections=cfg.REDIS.max_connections,
            host=cfg.REDIS.host,
            port=cfg.REDIS.port,
            db=db,
            password=cfg.REDIS.password,
            decode_responses=True
        )
        self._functools = MyRedisFunction()

    def open(self, db: int = 0):
        self._pool.connection_kwargs["db"] = db
        self._functools.conn = StrictRedis(connection_pool=self._pool, db=db)
        return self._functools

    def __enter__(self, db: int = 0):
        self.open(db)
        return self._functools

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._functools.close()


class MyRedisFunction:

    def __init__(self, conn: StrictRedis = None):
        self.conn = conn

    def close(self):
        if self.conn:
            self.conn.close()

    def subscribe(self, **kwargs):
        """订阅频道"""
        pub = self.conn.pubsub(ignore_subscribe_messages=True)
        pub.subscribe(**kwargs)
        pub.run_in_thread()

    def publish(self, channel: str, message: Union[str, dict]):
        """发布消息"""
        self.conn.publish(channel, dumps(message) if isinstance(message, dict) else message)

    def set(self, key: str, value: Union[str, int, float, dict], timeout: float = None):
        """写入"""
        self.conn.set(key, dumps(value) if isinstance(value, dict) else value, ex=timeout)

    def get(self, key: str, load: bool = True) -> Union[str, int, float, dict]:
        """读取"""
        data = self.conn.get(key)
        if load:
            return loads(data) if data else None
        return data

    def delete(self, key: str):
        """删除"""
        self.conn.delete(key)

    def hset(self, name: str, key: Union[str, int, float], value: Union[str, int, float, dict]):
        """哈希写入"""
        self.conn.hset(name, key, dumps(value) if isinstance(value, dict) else value)

    def hget(self, name: str, key: Union[str, int, float, list] = None, load: bool = True) -> Union[str, int, float, dict]:
        """哈希读取"""
        if key:
            if isinstance(key, list):
                data = self.conn.hmget(name, keys=key)
            else:
                data = self.conn.hget(name, key=key)
            return loads(data) if load else data
        else:
            return self.conn.hgetall(name)

    def hdel(self, name: str, key: str = None, ):
        """哈希删除"""
        self.conn.hdel(name, key)


if __name__ == '__main__':
    pass

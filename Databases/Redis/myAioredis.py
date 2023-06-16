# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/3/22 20:23

from typing import Union

from ujson import loads, dumps
from aioredis import ConnectionPool, StrictRedis

from Configure import cfg


class MyAioredis:

    def __init__(self, db: int = 0):
        self._pool = ConnectionPool(
            max_connections=cfg.REDIS.max_connections,
            host=cfg.REDIS.host,
            port=cfg.REDIS.port,
            db=db,
            password=cfg.REDIS.password,
            decode_responses=True
        )
        self._functools = MyAioredisFunctools()

    async def open(self, db: int = 0):
        self._pool.connection_kwargs["db"] = db
        self._functools.conn = await StrictRedis(connection_pool=self._pool)
        return self._functools

    async def __aenter__(self, db: int = 0):
        await self.open(db)
        return self._functools

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._functools.close()


class MyAioredisFunctools:

    def __init__(self, connection: StrictRedis = None):
        self.conn = connection

    async def close(self):
        if self.conn:
            await self.conn.close()

    async def publish(self, channel: str, message: Union[str, dict]):
        await self.conn.publish(channel, message=dumps(message) if isinstance(message, dict) else message)

    async def subscribe(self, **kwargs):
        pub = self.conn.pubsub(ignore_subscribe_messages=True)
        await pub.subscribe(**kwargs)
        await pub.run()

    async def set(self, key: str, value: Union[str, int, float, dict], timeout: float = None):
        await self.conn.set(name=key, value=dumps(value) if isinstance(value, dict) else value, ex=timeout)

    async def get(self, key: str, load: bool = True) -> Union[str, int, float, dict]:
        data = await self.conn.get(name=key)
        if load:
            return loads(data) if data else None
        return data

    async def delete(self, key: str):
        await self.conn.delete(key)

    async def hset(self, name: str, key: Union[str, int, float], value: Union[str, int, float, dict]):
        await self.conn.hset(name=name, key=key, value=dumps(value) if isinstance(value, dict) else value)

    async def hget(self, name: str, key: Union[str, int, float, list] = None, load: bool = True) -> Union[str, int, float, dict]:
        if key:
            if isinstance(key, list):
                data = await self.conn.hmget(name=name, keys=key)
            else:
                data = await self.conn.hget(name=name, key=key)
            return loads(data) if load else data
        else:
            return await self.conn.hgetall(name=name)

    async def hdel(self, name: str, key: Union[str, int, float, list]):
        await self.conn.hdel(name, key)


if __name__ == '__main__':
    pass

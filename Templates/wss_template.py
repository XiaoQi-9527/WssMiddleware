# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/6/14 18:32

from loguru import logger as log
from typing import Dict, List

from uvloop import EventLoopPolicy
from asyncio import set_event_loop_policy, get_event_loop, sleep, gather
from collections import namedtuple

from Functools import WebsocketClient, MyDatetime
from Databases import MyAioredis, MyAioredisFunctools
from Models import SubscribeConfigModel

set_event_loop_policy(EventLoopPolicy())

ToSub = namedtuple("ToSub", ("id", "symbol", "status", "business", "params"))


class WssTemplate(WebsocketClient):

    def __init__(self, conn: MyAioredisFunctools = None):
        super().__init__()

        # loop
        self.loop = get_event_loop()

        # redis
        self.redis_pool = MyAioredis()
        self.redis_conn = conn

        # mysql
        self.subscribe_cfg_model = SubscribeConfigModel()

        # constant
        self.type: str = "spot"
        self.url: str = ""
        self.exchange: str = ""
        self.symbol_mapping: Dict[str, str] = {}  # 币对对照表

        self.symbol_last_depth: dict = {}
        self.symbol_last_kline: dict = {}

        self.current_subscribe_depth: list = []
        self.current_subscribe_kline: list = []

    async def init_redis_conn(self, db: int = 0):
        self.redis_conn = await self.redis_pool.open(db=db)

    def init_symbol(self, symbol: str):
        raise NotImplementedError

    @staticmethod
    def add_time(val: dict, dt=None):
        val["update_ts"] = MyDatetime.dt2ts(dt, thousand=True),
        val["update_dt"] = MyDatetime.dt2str(dt)
        return val

    async def on_cache(self, db: int = 0):
        while True:
            conn = await self.redis_pool.open(db=db)
            try:
                while True:
                    try:
                        dt = MyDatetime.now()
                        last_depth = self.symbol_last_depth.copy()
                        task1 = [
                            conn.hset(
                                name=f"EXCHANGE-SPOT-WSS-DEPTH-{symbol}",
                                key=self.exchange,
                                value=self.add_time(value, dt)
                            )
                            for symbol, value in last_depth.items()
                        ]
                        last_kline = self.symbol_last_kline.copy()
                        task2 = [
                            conn.hset(
                                name=f"EXCHANGE-SPOT-WSS-KLINE-{symbol}",
                                key=self.exchange,
                                value=self.add_time(value, dt)
                            )
                            for symbol, value in last_kline.items()
                        ]
                        await gather(*task1, *task2)
                    except Exception as e:
                        log.warning(f"set_value, err: {e}")
                        raise e
                    else:
                        del dt, last_depth, last_kline, task1, task2
                    finally:
                        await sleep(0.5)
            except Exception as e:
                log.warning(f"on_cache, err: {e}")
            finally:
                await conn.close()
                del conn
                await sleep(1)

    async def get_data_from_mysql(self) -> List[ToSub]:
        try:
            sql = SubscribeConfigModel.select(
                SubscribeConfigModel.id,
                SubscribeConfigModel.symbol,
                SubscribeConfigModel.status,
                SubscribeConfigModel.business,
                SubscribeConfigModel.params,
            ).where(
                (SubscribeConfigModel.exchange == self.exchange)
                &
                (SubscribeConfigModel.type == self.type)
            )
            query = await self.subscribe_cfg_model.object.execute(sql.dicts())
        except Exception as e:
            log.warning(f"get_data_from_mysql, err: {e}")
            return []
        else:
            return list(map(lambda x: ToSub(**x), query))
        finally:
            pass

    async def on_task(self):
        try:
            to_sub = await self.get_data_from_mysql()
            for item in to_sub:
                try:
                    if "depth" in item.business:
                        if item.status:
                            if item.symbol not in self.current_subscribe_depth:
                                await self.subscribe_depth(item)
                                self.current_subscribe_depth.append(item.symbol)
                                log.info(f"current_sub_depth, id: {item.id}, symbol: {item.symbol}")
                        else:
                            if item.symbol in self.current_subscribe_depth:
                                await self.subscribe_depth(item)
                                self.current_subscribe_depth.remove(item.symbol)
                    if "kline" in item.business:
                        if item.status:
                            if item.symbol not in self.current_subscribe_kline:
                                await self.subscribe_kline(item)
                                self.current_subscribe_kline.append(item.symbol)
                                log.info(f"current_sub_kline, id: {item.id}, symbol: {item.symbol}")
                        else:
                            if item.symbol in self.current_subscribe_kline:
                                await self.subscribe_kline(item)
                                self.current_subscribe_kline.remove(item.symbol)
                except Exception as e:
                    log.warning(f"订阅处理, symbol: {item.symbol}, err: {e}")
                finally:
                    await sleep(0.2)
            log.info(f"current_sub_depth_length: {len(self.current_subscribe_depth)}")
            log.info(f"current_sub_kline_length: {len(self.current_subscribe_kline)}")
        except Exception as e:
            log.warning(f"on_task, err: {e}")
        else:
            del to_sub
            log.info(f"on_task, ok")
        finally:
            pass

    async def subscribe_depth(self, item: ToSub, depth: int = 5):
        raise NotImplementedError

    async def subscribe_kline(self, item: ToSub, interval: str = "1m"):
        raise NotImplementedError

    async def on_connected(self):
        await self.redis_conn.close()
        await self.init_redis_conn()
        self.current_subscribe_depth = []
        self.current_subscribe_kline = []

    async def on_first(self):
        await self.init_session()
        await self.init_redis_conn()

    async def on_timer(self):
        while True:
            try:
                if not self.is_connected:
                    continue
                await self.on_task()
            finally:
                await sleep(5)

    def run(self):
        self.loop.run_until_complete(self.on_first())
        self.loop.create_task(self.on_timer())
        self.loop.create_task(self.on_cache())
        self.loop.create_task(self.subscribe(url=self.url))
        self.loop.run_forever()


if __name__ == "__main__":
    pass

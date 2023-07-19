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

        # dt
        self.MDT = MyDatetime

        # redis
        self.redis_db: int = 1
        self.redis_pool = MyAioredis()
        self.redis_conn = conn

        # mysql
        self.subscribe_cfg_model = SubscribeConfigModel()

        # constant
        self.type: str = "spot"
        self.url: str = ""
        self.exchange: str = ""
        self.to_subscribe: Dict[str, ToSub] = {}
        self.symbol_mapping: Dict[str, str] = {}  # 币对对照表

        self.symbol_last_depth: dict = {}
        self.symbol_last_kline: dict = {}
        self.symbol_last_trade: dict = {}
        self.symbol_last_ticker: dict = {}

        self.current_subscribe_depth: list = []
        self.current_subscribe_kline: list = []
        self.current_subscribe_trade: list = []
        self.current_subscribe_ticker: list = []

    async def init_redis_conn(self):
        self.redis_conn = await self.redis_pool.open(db=self.redis_db)

    def init_symbol(self, symbol: str):
        raise NotImplementedError

    def add_time(self, val: dict, dt=None):
        val["update_ts"] = self.MDT.dt2ts(dt, thousand=True)
        val["update_dt"] = self.MDT.dt2str(dt)
        return val

    def create_task_4_cache(self, conn, dt, task: str, data: dict):
        if not data:
            return []
        return [
            conn.hset(
                name=f"EXCHANGE-SPOT-WSS-{task}-{symbol}".upper(),
                key=self.exchange,
                value=self.add_time(value, dt)
            )
            for symbol, value in data.items()
        ]

    async def on_cache(self):
        while True:
            conn = await self.redis_pool.open(db=self.redis_db)
            try:
                while True:
                    try:
                        dt = self.MDT.now()
                        await gather(
                            *self.create_task_4_cache(conn, dt, task="DEPTH", data=self.symbol_last_depth.copy()),
                            *self.create_task_4_cache(conn, dt, task="KLINE", data=self.symbol_last_kline.copy()),
                            *self.create_task_4_cache(conn, dt, task="TRADE", data=self.symbol_last_trade.copy()),
                            *self.create_task_4_cache(conn, dt, task="TICKER", data=self.symbol_last_ticker.copy()),
                        )
                    except Exception as e:
                        log.warning(f"set_value, err: {e}")
                        raise e
                    else:
                        del dt
                    finally:
                        await sleep(0.5)
            except Exception as e:
                log.warning(f"on_cache, err: {e}")
            finally:
                await conn.close()
                del conn
                await sleep(1)

    async def get_data_from_mysql(self):
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
            self.to_subscribe = {v.symbol: v for v in map(lambda x: ToSub(**x), query)}
        except Exception as e:
            log.warning(f"get_data_from_mysql, err: {e}")
        else:
            del sql, query
        finally:
            pass

    async def switch_task_by_channel(self, channel: str, current_sub: list, symbol: str, item: ToSub):
        if item.status:
            if symbol not in current_sub:
                await self.subscribe_by_channel(channel=channel, item=item)
                current_sub.append(symbol)
                log.info(f"current_sub_{channel}, id: {item.id}, symbol: {symbol}")
                await sleep(0.2)
        else:
            if symbol in current_sub:
                await self.subscribe_by_channel(channel, item)
                current_sub.remove(symbol)
                log.info(f"current_un_sub_{channel}, id: {item.id}, symbol: {symbol}")
                await sleep(0.2)
        return current_sub

    async def on_task(self):
        try:
            await self.get_data_from_mysql()
            for symbol, item in self.to_subscribe.items():
                try:
                    if "depth" in item.business:
                        self.current_subscribe_depth = await self.switch_task_by_channel(
                            channel="depth", current_sub=self.current_subscribe_depth, symbol=symbol, item=item
                        )
                    if "kline" in item.business:
                        self.current_subscribe_kline = await self.switch_task_by_channel(
                            channel="kline", current_sub=self.current_subscribe_kline, symbol=symbol, item=item
                        )
                    if "trade" in item.business:
                        self.current_subscribe_trade = await self.switch_task_by_channel(
                            channel="trade", current_sub=self.current_subscribe_trade, symbol=symbol, item=item
                        )
                    if "ticker" in item.business:
                        self.current_subscribe_ticker = await self.switch_task_by_channel(
                            channel="ticker", current_sub=self.current_subscribe_ticker, symbol=symbol, item=item
                        )
                except Exception as e:
                    log.warning(f"订阅处理, symbol: {symbol}, err: {e}")
        except Exception as e:
            log.warning(f"on_task, err: {e}")
        else:
            log.info(f"on_task, ok")
        finally:
            log.info(f"current_depth_length: {len(self.current_subscribe_depth)}")
            log.info(f"current_kline_length: {len(self.current_subscribe_kline)}")
            log.info(f"current_trade_length: {len(self.current_subscribe_trade)}")
            log.info(f"current_ticker_length: {len(self.current_subscribe_ticker)}")

    async def subscribe_by_channel(self, channel: str, item: ToSub):
        raise NotImplementedError

    async def on_connected(self):
        await self.redis_conn.close()
        await self.init_redis_conn()
        self.current_subscribe_depth = []
        self.current_subscribe_kline = []
        self.current_subscribe_trade = []
        self.current_subscribe_ticker = []

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

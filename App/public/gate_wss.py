# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023.06.14 21:12

import sys
sys.path.append("/root/WssMiddleware")

from loguru import logger as log

from asyncio import sleep

from Objects import Depth, KLine
from Constants import Hosts
from Functools import MyDatetime
from Templates import WssTemplate, ToSub


class GateWssPublic(WssTemplate):

    def __init__(self):
        super().__init__()

        # constants
        self.url: str = Hosts.GATE.data_wss
        self.exchange: str = "gate"

    def init_symbol(self, symbol: str):
        new_symbol = symbol.upper()
        self.symbol_mapping[new_symbol] = symbol
        return new_symbol

    async def subscribe_depth(self, item: ToSub, depth: int = 5):
        action = "subscribe" if item.status else "unsubscribe"
        await self.send_packet({
            "time": int(MyDatetime.timestamp()),
            "channel": "spot.order_book",
            "event": action,
            "payload": [
                self.init_symbol(item.symbol), str(depth), "1000ms",
            ]
        })
        del action

    async def subscribe_kline(self, item: ToSub, interval: str = "1m"):
        action = "subscribe" if item.status else "unsubscribe"
        await self.send_packet({
            "time": int(MyDatetime.timestamp()),
            "channel": "spot.candlesticks",
            "event": action,
            "payload": [
                interval, self.init_symbol(item.symbol)
            ]
        })
        del action

    async def on_packet(self, data: dict):
        event: str = data.get("event", "")
        if event == "subscribe":
            return await self.on_check(data)
        if event == "update":
            channel: str = data.get("channel", "")
            if channel == "spot.order_book":
                self.loop.create_task(self.on_depth(data))
            elif channel == "spot.candlesticks":
                self.loop.create_task(self.on_kline(data))
            del channel
        del event

    async def on_check(self, data: dict):
        pass

    @staticmethod
    def _init4depth(lst: list) -> dict:
        return {i: Depth(price=float(v[0]), amount=float(v[1]))._asdict() for i, v in enumerate(lst, 1)}

    async def on_depth(self, data: dict):
        try:
            depth: dict = data.get("result", {})
            if not depth:
                return
            symbol: str = self.symbol_mapping[depth["s"]].upper()
            bid: list = depth.get("bids", [[0, 0]])[0]
            ask: list = depth.get("asks", [[0, 0]])[0]
            self.symbol_last_depth[symbol] = {
                "depth": {
                    # "bids": self._init4depth(depth.get("bids", [])),
                    # "asks": self._init4depth(depth.get("asks", [])),
                    "bids": {"price": float(bid[0]), "amount": float(bid[1])},
                    "asks": {"price": float(ask[0]), "amount": float(ask[1])},
                }
            }
        except Exception as e:
            log.warning(f"depth err: {e}, data: {data}")
        else:
            del symbol, bid, ask
        finally:
            del depth

    async def on_kline(self, data: dict):
        try:
            kline: dict = data.get("result", {})
            if not kline:
                return
            symbol: str = self.symbol_mapping["_".join(kline["n"].split("_")[1:]).lower()].upper()
            self.symbol_last_kline[symbol] = {
                "kline": KLine(
                    open=float(kline["o"]),
                    high=float(kline["h"]),
                    low=float(kline["l"]),
                    close=float(kline["c"]),
                    volume=float(kline["v"]),
                    amount=float(kline["a"]),
                    num=-1,
                )._asdict()
            }
        except Exception as e:
            log.warning(f"kline err: {e}, data: {data}")
        else:
            del symbol
        finally:
            del kline

    async def on_ping(self, data: dict = None):
        """
        {'time': 1683797041, 'time_ms': 1683797041040, 'channel': 'spot.pong', 'event': '', 'result': None}
        """
        while True:
            try:
                if self.is_connected:
                    await self.send_packet({"time": int(MyDatetime.timestamp()), "channel": "spot.ping"})
            except Exception as e:
                log.warning(f"on_ping, err: {e}")
            finally:
                await sleep(30)

    def run(self):
        self.loop.run_until_complete(self.on_first())
        self.loop.create_task(self.on_timer())
        self.loop.create_task(self.on_cache())
        self.loop.create_task(self.subscribe(url=self.url))
        self.loop.create_task(self.on_ping())
        self.loop.run_forever()


if __name__ == "__main__":
    GateWssPublic().run()

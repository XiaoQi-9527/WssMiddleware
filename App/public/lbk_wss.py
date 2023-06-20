# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023.06.14 21:25

import sys
sys.path.append("/root/WssMiddleware")

from loguru import logger as log

from Objects import Depth, KLine
from Constants import Hosts
from Templates import WssTemplate, ToSub


class LbkWssPublic(WssTemplate):

    def __init__(self):
        super().__init__()

        # constants
        self.url: str = Hosts.LBK.data_wss
        self.exchange: str = "lbank"

    async def subscribe_depth(self, item: ToSub, depth: int = 5):
        action = "subscribe" if item.status else "unsubscribe"
        await self.send_packet({
            "action": action,
            "subscribe": "depth",
            "depth": str(depth),
            "pair": item.symbol.lower()
        })
        del action

    async def subscribe_kline(self, item: ToSub, interval: str = "1min"):
        action = "subscribe" if item.status else "unsubscribe"
        await self.send_packet({
            "action": action,
            "subscribe": "kbar",
            "kbar": interval,
            "pair": item.symbol.lower()
        })
        del action

    async def on_packet(self, data: dict):
        if data.get("action", None) == "ping":
            return await self.on_ping(data)
        if data.get("status", None) == "error":
            return await self.on_check(data)
        _type: str = data.get("type", None)
        if _type == "depth":
            await self.on_depth(data)
        elif _type == "kbar":
            await self.on_kline(data)
        else:
            pass
        del _type

    async def on_check(self, data: dict):
        pass

    async def on_ping(self, data: dict):
        log.info(f"ping: {data}")
        await self.send_packet({"action": "pong", "pong": data["ping"]})

    @staticmethod
    def _init4depth(lst: list) -> dict:
        return {i: Depth(price=float(v[0]), amount=float(v[1]))._asdict() for i, v in enumerate(lst, 1)}

    async def on_depth(self, data: dict):
        try:
            symbol: str = data.get("pair", "").lower()
            depth: dict = data.get("depth", {})
            if not depth:
                return
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
            del bid, ask
        finally:
            del symbol, depth

    async def on_kline(self, data: dict):
        try:
            symbol: str = data.get("pair", "").lower()
            kline: dict = data.get("kbar", {})
            if not kline:
                return
            self.symbol_last_kline[symbol] = {
                "kline": KLine(
                    open=float(kline["o"]),
                    high=float(kline["h"]),
                    low=float(kline["l"]),
                    close=float(kline["c"]),
                    volume=float(kline["v"]),
                    amount=float(kline["a"]),
                    num=float(kline["n"]),
                )._asdict()
            }
        except Exception as e:
            log.warning(f"kline err: {e}, data: {data}")
        finally:
            del symbol, kline


if __name__ == "__main__":
    LbkWssPublic().run()

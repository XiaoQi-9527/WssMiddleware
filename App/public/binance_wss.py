# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/6/14 18:37

import sys
sys.path.append("/root/WssMiddleware")

from loguru import logger as log

from Objects import Depth, KLine, Ticker
from Constants import Hosts
from Templates import WssTemplate, ToSub


class BinanceWssPublic(WssTemplate):

    def __init__(self):
        super().__init__()

        # constants
        self.url: str = Hosts.BINANCE.data_wss
        self.exchange: str = "binance"

    def init_symbol(self, symbol: str):
        new_symbol = symbol.replace("_", "").lower()
        self.symbol_mapping[new_symbol] = symbol
        return new_symbol

    async def subscribe_depth(self, item: ToSub, depth: int = 5):
        action = "SUBSCRIBE" if item.status else "UNSUBSCRIBE"
        await self.send_packet({
            "method": action,
            "params": [
                f"{self.init_symbol(item.symbol)}@depth{depth}@1000ms"
            ],
            "id": item.id
        })
        del action

    async def subscribe_kline(self, item: ToSub, interval: str = "1m"):
        action = "SUBSCRIBE" if item.status else "UNSUBSCRIBE"
        await self.send_packet({
            "method": action,
            "params": [
                f"{self.init_symbol(item.symbol)}@kline_{interval}"
            ],
            "id": item.id + 10000
        })
        del action

    async def subscribe_ticker(self, item: ToSub):
        action = "SUBSCRIBE" if item.status else "UNSUBSCRIBE"
        await self.send_packet({
            "method": action,
            "params": [
                f"{self.init_symbol(item.symbol)}@ticker"
            ],
            "id": item.id + 20000
        })
        del action

    async def on_packet(self, data: dict):
        if "id" in data.keys():
            return await self.on_check(data)
        if "depth" in data["stream"]:
            self.loop.create_task(self.on_depth(data))
        elif "kline" in data["stream"]:
            self.loop.create_task(self.on_kline(data))
        elif "ticker" in data["stream"]:
            self.loop.create_task(self.on_ticker(data))

    async def on_check(self, data: dict):
        pass

    @staticmethod
    def _init4depth(lst: list) -> dict:
        return {str(i): Depth(price=float(v[0]), amount=float(v[1]))._asdict() for i, v in enumerate(lst, 1)}

    async def on_depth(self, data: dict):
        try:
            symbol: str = self.symbol_mapping[data["stream"].split("@")[0].lower()].upper()
            depth: dict = data.get("data", {})
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
            # await self.redis_conn.hset(name=f"EXCHANGE-SPOT-WSS-DEPTH-{symbol}", key=self.exchange, value=res)
        except Exception as e:
            log.warning(f"depth err: {e}, data: {data}")
        else:
            del bid, ask
        finally:
            del symbol, depth

    async def on_kline(self, data: dict):
        try:
            symbol: str = self.symbol_mapping[data["stream"].split("@")[0].lower()].upper()
            kline: dict = data.get("data", {}).get("k", {})
            if not kline:
                return
            self.symbol_last_kline[symbol] = {
                "kline": KLine(
                    open=float(kline["o"]),
                    high=float(kline["h"]),
                    low=float(kline["l"]),
                    close=float(kline["c"]),
                    volume=float(kline["v"]),
                    amount=float(kline["q"]),
                    num=float(kline["n"]),
                )._asdict()
            }
            # await self.redis_conn.hset(name=f"EXCHANGE-SPOT-WSS-KLINE-{symbol}", key=self.exchange, value=res)
        except Exception as e:
            log.warning(f"kline err: {e}, data: {data}")
        finally:
            del symbol, kline

    async def on_ticker(self, data: dict):
        try:
            symbol: str = self.symbol_mapping[data["stream"].split("@")[0].lower()].upper()
            ticker: dict = data.get("data", {})
            if not ticker:
                return
            self.symbol_last_ticker[symbol] = {
                "ticker": Ticker(
                    high=float(ticker["h"]),
                    low=float(ticker["l"]),
                    volume=float(ticker["v"]),
                    quote=float(ticker["q"]),
                    latest_price=float(ticker["c"]),
                    timestamp=int(ticker["E"])
                )._asdict()
            }
            # await self.redis_conn.hset(name=f"EXCHANGE-SPOT-WSS-TICKER-{symbol}", key=self.exchange, value=res)
        except Exception as e:
            log.warning(f"ticker err: {e}, data: {data}")
        finally:
            del symbol, ticker


if __name__ == "__main__":
    BinanceWssPublic().run()

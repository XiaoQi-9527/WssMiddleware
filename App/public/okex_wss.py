# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023.06.14 21:25

import sys
sys.path.append("/root/WssMiddleware")

from loguru import logger as log

from Objects import Depth, KLine, Ticker
from Constants import Hosts
from Templates import WssTemplate, ToSub


class OkexWssPublic(WssTemplate):

    def __init__(self):
        super().__init__()

        # constants
        self.url: str = Hosts.OKEX.data_wss
        self.exchange: str = "okex"

    def init_symbol(self, symbol: str):
        new_symbol = symbol.replace("_", "-").upper()
        self.symbol_mapping[new_symbol] = symbol
        return new_symbol

    async def subscribe_depth(self, item: ToSub, depth: int = 5):
        action = "subscribe" if item.status else "unsubscribe"
        await self.send_packet({
            "op": action,
            "args": [{
                "channel": f"books{depth}",
                "instId": self.init_symbol(item.symbol)
            }]
        })
        del action

    async def subscribe_kline(self, item: ToSub, interval: str = "1M"):
        action = "subscribe" if item.status else "unsubscribe"
        await self.send_packet({
            "op": action,
            "args": [{
                "channel": f"candle{interval}",
                "instId": self.init_symbol(item.symbol)
            }]
        })
        del action

    async def subscribe_ticker(self, item: ToSub):
        action = "subscribe" if item.status else "unsubscribe"
        await self.send_packet({
            "op": action,
            "args": [{
                "channel": "tickers",
                "instId": self.init_symbol(item.symbol)
            }]
        })
        del action

    async def on_packet(self, data: dict):
        if "event" in data.keys():
            return await self.on_check(data)
        channel: str = data.get("arg", {}).get("channel", "")
        if channel.startswith("books"):
            self.loop.create_task(self.on_depth(data))
        elif channel.startswith("candle"):
            self.loop.create_task(self.on_kline(data))
        elif channel.startswith("tickers"):
            self.loop.create_task(self.on_ticker(data))
        del channel

    async def on_check(self, data: dict):
        pass

    @staticmethod
    def _init4depth(lst: list) -> dict:
        return {i: Depth(price=float(v[0]), amount=float(v[1]))._asdict() for i, v in enumerate(lst, 1)}

    async def on_depth(self, data: dict):
        try:
            symbol: str = self.symbol_mapping[data.get("arg", {}).get("instId", "").upper()]
            depth: dict = data.get("data", [{}])[0]
            if not depth:
                return
            bid: list = depth.get("bids", [[0, 0, 0, 0]])[0]
            ask: list = depth.get("asks", [[0, 0, 0, 0]])[0]
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
            symbol: str = self.symbol_mapping[data.get("arg", {}).get("instId", "").upper()]
            kline: list = data.get("data", [[]])[0]
            if not kline:
                return
            self.symbol_last_kline[symbol] = {
                "kline": KLine(
                    open=float(kline[1]),
                    high=float(kline[2]),
                    low=float(kline[3]),
                    close=float(kline[4]),
                    volume=float(kline[5]),
                    amount=float(kline[6]),
                    num=-1,
                )._asdict()
            }
        except Exception as e:
            log.warning(f"kline err: {e}, data: {data}")
        finally:
            del symbol, kline

    async def on_ticker(self, data: dict):
        try:
            symbol: str = self.symbol_mapping[data.get("arg", {}).get("instId", "").upper()]
            ticker: dict = data.get("data", [{}])[0]
            if not ticker:
                return
            self.symbol_last_ticker[symbol] = {
                "ticker": Ticker(
                    high=float(ticker["high24h"]),
                    low=float(ticker["low24h"]),
                    volume=float(ticker["vol24h"]),
                    quote=float(ticker["volCcy24h"]),
                    latest_price=float(ticker["last"]),
                    timestamp=int(ticker["ts"])
                )._asdict()
            }
        except Exception as e:
            log.warning(f"ticker err: {e}, data: {data}")
        finally:
            del symbol, ticker


if __name__ == "__main__":
    OkexWssPublic().run()

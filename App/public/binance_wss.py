# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/6/14 18:37

import sys
sys.path.append("/root/WssMiddlewareV2")

from loguru import logger as log

from Functools import define
from Objects import Depth, KLine, Trade, Ticker
from Constants import Hosts
from Templates import WssTemplate, ToSub


class BinanceWssPublic(WssTemplate):

    def __init__(self, channel: str):
        super().__init__()

        # constants
        self.channel = channel.lower()
        self.url: str = Hosts.BINANCE.data_wss
        self.exchange: str = "binance"

        self.channel_4_sub: str = {
            "depth": "{symbol}@depth{depth}@1000ms",    # depth: 5
            "kline": "{symbol}@kline_{interval}",       # interval: 1m
            "trade": "{symbol}@trade",
            "ticker": "{symbol}@ticker",
        }[self.channel]

    def init_symbol(self, symbol: str):
        new_symbol = symbol.replace("_", "").lower()
        self.symbol_mapping[new_symbol] = symbol
        return new_symbol

    async def subscribe_by_channel(self, item: ToSub):
        msg: dict = {
            "method": "SUBSCRIBE" if item.status else "UNSUBSCRIBE",
            "params": [],
            "id": item.id,
        }
        if self.channel == "depth":
            param = self.channel_4_sub.format(symbol=self.init_symbol(item.symbol), depth="5")
        elif self.channel == "kline":
            param = self.channel_4_sub.format(symbol=self.init_symbol(item.symbol), interval="1m")
            msg["id"] += 10000
        elif self.channel == "trade":
            param = self.channel_4_sub.format(symbol=self.init_symbol(item.symbol))
            msg["id"] += 20000
        elif self.channel == "ticker":
            param = self.channel_4_sub.format(symbol=self.init_symbol(item.symbol))
            msg["id"] += 30000
        else:
            return
        msg["params"].append(param)
        await self.send_packet(msg)
        del msg, param

    async def on_packet(self, data: dict):
        if "id" in data.keys():
            return await self.on_check(data)
        if "depth" in data["stream"]:
            self.loop.create_task(self.on_depth(data))
        elif "kline" in data["stream"]:
            self.loop.create_task(self.on_kline(data))
        elif "trade" in data["stream"]:
            self.loop.create_task(self.on_trade(data))
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
            self.symbol_last_data[symbol] = {
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
            symbol: str = self.symbol_mapping[data["stream"].split("@")[0].lower()].upper()
            kline: dict = data.get("data", {}).get("k", {})
            if not kline:
                return
            self.symbol_last_data[symbol] = {
                "kline": KLine(
                    open=float(kline["o"]),
                    high=float(kline["h"]),
                    low=float(kline["l"]),
                    close=float(kline["c"]),
                    volume=float(kline["v"]),
                    amount=float(kline["q"]),
                    num=float(kline["n"]),
                    timestamp=kline["t"]
                )._asdict()
            }
        except Exception as e:
            log.warning(f"kline err: {e}, data: {data}")
        finally:
            del symbol, kline

    async def on_trade(self, data: dict):
        try:
            symbol: str = self.symbol_mapping[data["stream"].split("@")[0].lower()].upper()
            trade: dict = data.get("data", {})
            if not trade:
                return
            self.symbol_last_data[symbol] = {
                "trade": Trade(
                    amount=float(trade["q"]),
                    price=float(trade["p"]),
                    volume=float(trade["q"]) * float(trade["p"]),
                    direction="sell" if trade["m"] else "buy",
                    timestamp=trade["T"]
                )._asdict()
            }
        except Exception as e:
            log.warning(f"trade err: {e}, data: {data}")
        finally:
            del symbol, trade

    async def on_ticker(self, data: dict):
        try:
            symbol: str = self.symbol_mapping[data["stream"].split("@")[0].lower()].upper()
            ticker: dict = data.get("data", {})
            if not ticker:
                return
            self.symbol_last_data[symbol] = {
                "ticker": Ticker(
                    high=float(ticker["h"]),
                    low=float(ticker["l"]),
                    volume=float(ticker["v"]),
                    quote=float(ticker["q"]),
                    latest_price=float(ticker["c"]),
                    timestamp=int(ticker["E"])
                )._asdict()
            }
        except Exception as e:
            log.warning(f"ticker err: {e}, data: {data}")
        finally:
            del symbol, ticker


if __name__ == "__main__":
    cn = define(name="channel", default="depth", _type=str)
    BinanceWssPublic(channel=cn).run()

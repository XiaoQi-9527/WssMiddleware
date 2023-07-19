# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023.06.14 21:25

import sys
sys.path.append("/root/WssMiddlewareV2")

from loguru import logger as log

from Functools import define
from Objects import Depth, KLine, Trade, Ticker
from Constants import Hosts
from Templates import WssTemplate, ToSub


class OkexWssPublic(WssTemplate):

    def __init__(self, channel: str):
        super().__init__()

        # constants
        self.channel = channel.lower()
        self.url: str = Hosts.OKEX.data_wss
        self.exchange: str = "okex"

        self.channel_4_sub: str = {
            "depth": "books{depth}",        # depth: 5
            "kline": "candle{interval}",    # interval: 1M
            "trade": "trades",
            "ticker": "tickers",
        }[self.channel]

    def init_symbol(self, symbol: str):
        new_symbol = symbol.replace("_", "-").upper()
        self.symbol_mapping[new_symbol] = symbol
        return new_symbol

    async def subscribe_by_channel(self, item: ToSub):
        msg = {
            "op": "subscribe" if item.status else "unsubscribe",
            "args": [{
                "channel": "",
                "instId": self.init_symbol(item.symbol)
            }],
        }
        channel_string: str = self.channel_4_sub
        if self.channel == "depth":
            channel_string = channel_string.format(depth=5)
        elif self.channel == "kline":
            channel_string = channel_string.format(interval="1M")
        msg["args"][0]["channel"] = channel_string
        await self.send_packet(msg)
        del msg, channel_string

    async def on_packet(self, data: dict):
        if "event" in data.keys():
            return await self.on_check(data)
        channel: str = data.get("arg", {}).get("channel", "")
        if channel.startswith("books"):
            self.loop.create_task(self.on_depth(data))
        elif channel.startswith("candle"):
            self.loop.create_task(self.on_kline(data))
        elif channel.startswith("trades"):
            self.loop.create_task(self.on_trade(data))
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
            symbol: str = self.symbol_mapping[data.get("arg", {}).get("instId", "").upper()]
            kline: list = data.get("data", [[]])[0]
            if not kline:
                return
            self.symbol_last_data[symbol] = {
                "kline": KLine(
                    open=float(kline[1]),
                    high=float(kline[2]),
                    low=float(kline[3]),
                    close=float(kline[4]),
                    volume=float(kline[5]),
                    amount=float(kline[6]),
                    num=-1,
                    timestamp=int(kline[0])
                )._asdict()
            }
        except Exception as e:
            log.warning(f"kline err: {e}, data: {data}")
        finally:
            del symbol, kline

    async def on_trade(self, data: dict):
        try:
            symbol: str = self.symbol_mapping[data.get("arg", {}).get("instId", "").upper()]
            trade: dict = data.get("data", [{}])[0]
            if not trade:
                return
            self.symbol_last_data[symbol] = {
                "trade": Trade(
                    amount=float(trade["sz"]),
                    price=float(trade["px"]),
                    volume=float(trade["px"]) * float(trade["sz"]),
                    direction=trade["side"],
                    timestamp=trade["ts"],
                )._asdict()
            }
        except Exception as e:
            log.warning(f"trade err: {e}, data: {data}")
        finally:
            del symbol, trade

    #         WAVES_USDT
    async def on_ticker(self, data: dict):
        try:
            symbol: str = self.symbol_mapping[data.get("arg", {}).get("instId", "").upper()]
            ticker: dict = data.get("data", [{}])[0]
            if not ticker:
                return
            self.symbol_last_data[symbol] = {
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
    cn = define(name="channel", default="depth", _type=str)
    OkexWssPublic(channel=cn).run()

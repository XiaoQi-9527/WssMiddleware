# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023.06.14 21:25

import sys
sys.path.append("/root/WssMiddleware")

from loguru import logger as log

from asyncio import sleep

from Objects import Depth, KLine, Trade, Ticker
from Constants import Hosts
from Templates import WssTemplate, ToSub


class LbkWssPublic(WssTemplate):

    def __init__(self):
        super().__init__()

        # constants
        self.url: str = Hosts.LBK.data_wss
        self.exchange: str = "lbank"

        self.err_dict: dict = {
            "depth": [],
            "kline": [],
            "ticker": []
        }

        self.channel_map: dict = {
            "depth": "depth",       # depth: 5
            "kline": "kbar",        # interval: 1min
            "trade": "trade",
            "ticker": "tick",
        }

    async def subscribe_by_channel(self, channel: str, item: ToSub):
        msg: dict = {
            "action": "subscribe" if item.status else "unsubscribe",
            "subscribe": self.channel_map[channel],
            "pair": item.symbol.lower()
        }
        if channel == "depth":
            msg["depth"] = "5"
        elif channel == "kline":
            msg["kbar"] = "1min"
        await self.send_packet(msg)
        del msg

    async def on_packet(self, data: dict):
        if data.get("action", None) == "ping":
            return await self.on_ping(data)
        if data.get("status", None) == "error":
            return await self.on_check(data)
        _type: str = data.get("type", None)
        if _type == "depth":
            self.loop.create_task(self.on_depth(data))
        elif _type == "kbar":
            self.loop.create_task(self.on_kline(data))
        elif _type == "trade":
            self.loop.create_task(self.on_trade(data))
        elif _type == "tick":
            self.loop.create_task(self.on_ticker(data))
        else:
            pass
        del _type

    async def on_check(self, data: dict):
        try:
            symbol = data.get("message", "").split(":")[-1].replace("[", "").replace("]", "")
            log.warning(f"subscribe, symbol: {symbol}, err: {data}")
            item: ToSub = self.to_subscribe[symbol]
            if "depth" in item.business:
                try:
                    self.current_subscribe_depth.remove(symbol)
                except ValueError:
                    pass
                log.info(f"on_check, depth, 重新订阅异常币对: {symbol}")
            if "kline" in item.business:
                try:
                    self.current_subscribe_kline.remove(symbol)
                except ValueError:
                    pass
                log.info(f"on_check, kline, 重新订阅异常币对: {symbol}")
            if "trade" in item.business:
                try:
                    self.current_subscribe_trade.remove(symbol)
                except ValueError:
                    pass
                log.info(f"on_check, trade, 重新订阅异常币对: {symbol}")
            if "ticker" in item.business:
                try:
                    self.current_subscribe_ticker.remove(symbol)
                except ValueError:
                    pass
                log.info(f"on_check, ticker, 重新订阅异常币对: {symbol}")
        except Exception as e:
            log.warning(f"on_check, err: {e}")
        else:
            del symbol, item
        finally:
            pass

    async def on_ping(self, data: dict = None):
        if not data:
            msg = {"action": "ping", "ping": "ping.pong"}
            log.info(f"ping: {msg}")
        else:
            msg = {"action": "pong", "pong": data["ping"]}
            log.info(f"pong: {data}")
        await self.send_packet(msg)

    async def ping(self):
        while True:
            await sleep(10)
            await self.on_ping()

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
                    timestamp=self.MDT.dt2ts(dt=self.MDT.utc2dt(kline["t"]), thousand=True)
                )._asdict()
            }
        except Exception as e:
            log.warning(f"kline err: {e}, data: {data}")
        finally:
            del symbol, kline

    async def on_trade(self, data: dict):
        try:
            symbol: str = data.get("pair", "").lower()
            trade: dict = data.get("trade", {})
            if not trade:
                return
            self.symbol_last_trade[symbol] = {
                "trade": Trade(
                    amount=float(trade["amount"]),
                    price=float(trade["price"]),
                    volume=float(trade["volumePrice"]),
                    direction=trade["direction"].lower(),
                    timestamp=self.MDT.dt2ts(dt=self.MDT.utc2dt(trade["TS"]), thousand=True)
                )._asdict()
            }
        except Exception as e:
            log.warning(f"trade err: {e}, data: {data}")
        finally:
            del symbol, trade

    async def on_ticker(self, data: dict):
        try:
            symbol: str = data.get("pair", "").lower()
            ticker: dict = data.get("tick", {})
            if not ticker:
                return
            self.symbol_last_ticker[symbol] = {
                "ticker": Ticker(
                    high=float(ticker["high"]),
                    low=float(ticker["low"]),
                    volume=float(ticker["vol"]),
                    quote=float(ticker["turnover"]),
                    latest_price=float(ticker["latest"]),
                    timestamp=self.MDT.dt2ts(dt=self.MDT.utc2dt(data["TS"]), thousand=True)
                )._asdict()
            }
        except Exception as e:
            log.warning(f"ticker err: {e}, data: {data}")
        finally:
            del symbol, ticker

    def run(self):
        self.loop.run_until_complete(self.on_first())
        self.loop.create_task(self.on_timer())
        self.loop.create_task(self.on_cache())
        self.loop.create_task(self.subscribe(url=self.url))
        self.loop.create_task(self.ping())
        self.loop.run_forever()


if __name__ == "__main__":
    LbkWssPublic().run()

# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023.06.14 21:12

import sys
sys.path.append("/root/WssMiddleware")

from loguru import logger as log

from asyncio import sleep

from Objects import Depth, KLine, Trade, Ticker
from Constants import Hosts
from Templates import WssTemplate, ToSub


class GateWssPublic(WssTemplate):

    def __init__(self):
        super().__init__()

        # constants
        self.url: str = Hosts.GATE.data_wss
        self.exchange: str = "gate"

        self.channel_map: dict = {
            "depth": "spot.order_book",     # depth: 5
            "kline": "spot.candlesticks",   # interval: 1min
            "trade": "spot.trades",
            "ticker": "spot.tickers",
        }

    def init_symbol(self, symbol: str):
        new_symbol = symbol.upper()
        self.symbol_mapping[new_symbol] = symbol
        return new_symbol

    async def subscribe_by_channel(self, channel: str, item: ToSub):
        msg = {
            "time": int(self.MDT.timestamp()),
            "channel": self.channel_map[channel],
            "event": "subscribe" if item.status else "unsubscribe",
            "payload": []
        }
        if channel == "depth":
            msg["payload"] = [self.init_symbol(item.symbol), "5", "1000ms"]
        elif channel == "kline":
            msg["payload"] = ["1m", self.init_symbol(item.symbol)]
        elif channel == "trade":
            msg["payload"] = [self.init_symbol(item.symbol)]
        elif channel == "ticker":
            msg["payload"] = [self.init_symbol(item.symbol)]
        else:
            return
        await self.send_packet(msg)
        del msg

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
            elif channel == "spot.trades":
                self.loop.create_task(self.on_trade(data))
            elif channel == "spot.tickers":
                self.loop.create_task(self.on_ticker(data))
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
                    timestamp=int["t"] * 1000
                )._asdict()
            }
        except Exception as e:
            log.warning(f"kline err: {e}, data: {data}")
        else:
            del symbol
        finally:
            del kline

    async def on_trade(self, data: dict):
        try:
            trade: dict = data.get("result", {})
            if not trade:
                return
            symbol: str = self.symbol_mapping[trade["currency_pair"]].upper()
            self.symbol_last_trade[symbol] = {
                "trade": Trade(
                    amount=float(trade["amount"]),
                    price=float(trade["price"]),
                    volume=float(trade["amount"]) * float(trade["price"]),
                    direction=trade["side"].lower(),
                    timestamp=int(float(trade["create_time_ms"])),
                )
            }
        except Exception as e:
            log.warning(f"trade err: {e}, data: {data}")
        else:
            del symbol
        finally:
            del trade

    async def on_ticker(self, data: dict):
        try:
            ticker: dict = data.get("result", {})
            if not ticker:
                return
            symbol: str = self.symbol_mapping[ticker["currency_pair"]].upper()
            self.symbol_last_ticker[symbol] = {
                "ticker": Ticker(
                    high=float(ticker["high_24h"]),
                    low=float(ticker["low_24h"]),
                    volume=float(ticker["base_volume"]),
                    quote=float(ticker["quote_volume"]),
                    latest_price=float(ticker["last"]),
                    timestamp=int(data["time_ms"])
                )._asdict()
            }
        except Exception as e:
            log.warning(f"ticker err: {e}, data: {data}")
        else:
            del symbol
        finally:
            del ticker

    async def on_ping(self, data: dict = None):
        """
        {'time': 1683797041, 'time_ms': 1683797041040, 'channel': 'spot.pong', 'event': '', 'result': None}
        """
        while True:
            try:
                if self.is_connected:
                    await self.send_packet({"time": int(self.MDT.timestamp()), "channel": "spot.ping"})
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

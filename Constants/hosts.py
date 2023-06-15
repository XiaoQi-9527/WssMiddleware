# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/6/14 18:17

from dataclasses import dataclass


@dataclass(frozen=True)
class BINANCE:
    rest: str = "https://api.binance.com/"
    trade_wss: str = "wss://stream.binance.com:9443/ws/"
    data_wss: str = "wss://stream.binance.com:9443/stream"


@dataclass(frozen=True)
class GATE:
    rest: str = "https://api.gateio.ws"
    trade_wss: str = "wss://api.gateio.ws/ws/v4/"
    data_wss: str = "wss://api.gateio.ws/ws/v4/"


@dataclass(frozen=True)
class OKEX:
    rest: str = "https://www.okx.com"
    trade_wss: str = "wss://ws.okx.com:8443/ws/v5/private"
    data_wss: str = "wss://ws.okx.com:8443/ws/v5/public"


@dataclass(frozen=True)
class LBK:
    # rest: str = "http://10.10.10.85:99/v2/"
    # trade_wss: str = "ws://10.10.10.85:99/ws/V2/"
    # data_wss: str = "ws://10.10.10.85:99/ws/V2/"
    rest: str = "https://www.lbkex.net/v2/"
    trade_wss: str = "wss://www.lbkex.net/ws/V2/"
    data_wss: str = "wss://www.lbkex.net/ws/V2/"


@dataclass(frozen=True)
class Hosts:

    BINANCE = BINANCE
    GATE = GATE
    OKEX = OKEX
    LBK = LBK


if __name__ == "__main__":
    pass

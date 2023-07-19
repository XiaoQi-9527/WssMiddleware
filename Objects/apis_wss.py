# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/5/9 18:27

from collections import namedtuple

Depth = namedtuple(
    "Depth",
    (
        "price",    # 委托价
        "amount"    # 委托数量
    )
)

KLine = namedtuple(
    "KLine",
    (
        "open",         # 开
        "high",         # 高
        "low",          # 低
        "close",        # 收
        "volume",       # 成交量
        "amount",       # 成交额
        "num",          # 成交笔数
        "timestamp",    # 成交时间
    )
)

Trade = namedtuple(
    "Trade",
    (
        "amount",       # 成交数量
        "price",        # 成交价格
        "volume",       # 成交金额
        "direction",    # 成交方向: sell | buy
        "timestamp",    # 成交时间
    )
)

Ticker = namedtuple(
    "Ticker",
    (
        "high",             # 24hr最高价
        "low",              # 24hr最低价
        "volume",           # 24hr成交量
        "quote",            # 24hr成交额
        "latest_price",     # 最新成交价
        "timestamp",        # 更新时间
    )
)


if __name__ == "__main__":
    pass

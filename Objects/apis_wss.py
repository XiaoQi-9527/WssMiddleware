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
        "open",     # 开
        "high",     # 高
        "low",      # 低
        "close",    # 收
        "volume",   # 成交量
        "amount",   # 成交额
        "num",      # 成交笔数
    )
)


if __name__ == "__main__":
    pass

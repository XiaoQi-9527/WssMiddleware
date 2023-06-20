# WSS数据中间件 (server_id: 135)

## PUBLIC DATA

### DEPTH

```python
name = "EXCHANGE-SPOT-WSS-DEPTH-{symbol}".upper()  # symbol: btc_usdt
key = "exchange".lower()
value = {
    "depth": {
        "bids": {
            "price": 1.0,       # 委托价
            "amount": 100.01,   # 委托数量
        },
        "asks": {
            "price": 0.9,
            "amount": 100.09,
        }
    },
    "update_ts": 1686809977793,
    "update_dt": "2023-06-15 14:19:37"
}
```

### KLINE

```python
name = "EXCHANGE-SPOT-WSS-KLINE-{symbol}".upper()  # symbol: btc_usdt
key = "exchange".lower()
value = {
    "kline": {
        "open": 1.0,            # 开
        "high": 1.2,            # 高
        "low": 0.9,             # 低
        "close": 1.0,           # 收
        "volume": 100.01,       # 成交量
        "amount": 10000.01,     # 成交额
        "num": 10,              # 成交笔数
    },
    "update_ts": 1686809977793,
    "update_dt": "2023-06-15 14:19:37"
}
```


# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/3/29 00:17

from loguru import logger as log

import time
from ujson import loads, dumps
from asyncio import sleep
from aiohttp.http_websocket import WSMessage
from aiohttp import ClientSession


class WebsocketClient:

    def __init__(self, session: ClientSession = None):

        self._ws = None

        self.session = session
        self.is_connected: bool = False

    async def init_session(self):
        self.session = ClientSession(trust_env=True)

    async def on_ping(self, data: dict):
        raise NotImplementedError

    async def on_connected(self):
        raise NotImplementedError

    async def on_packet(self, data: dict):
        raise NotImplementedError

    async def send_packet(self, data: dict):
        try:
            await self._ws.send_str(dumps(data))
        except Exception as e:
            log.warning(f"send_packet, err: {e}")

    async def subscribe(self, url: str):
        while True:
            try:
                self._ws = await self.session.ws_connect(url=url, ssl=False)
                log.info(f"websocket 连接成功")
                await self.on_connected()
                self.is_connected = True
                async for msg in self._ws:  # type: WSMessage
                    try:
                        item: dict = msg.json(loads=loads)
                    except Exception as e:
                        log.warning(f"websocket data: {msg.data}, {e}")
                    else:
                        await self.on_packet(item)
                self._ws = None
                self.is_connected = False
                log.warning(f"websocket 断连, 即将重连")
                await sleep(0.2)
            except Exception as e:
                log.warning(f"websocket 异常: {e}, 即将重连")
                self.is_connected = False
                time.sleep(5)


if __name__ == '__main__':
    pass

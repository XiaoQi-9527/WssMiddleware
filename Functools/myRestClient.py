# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/3/29 00:20

from loguru import logger as log
from typing import Union

from ujson import loads
from dataclasses import dataclass
from aiohttp import ClientSession, ClientResponse


@dataclass
class Request:
    host: str
    api: str = ""
    method: str = ""
    params: dict = None
    payload: dict = None
    headers: dict = None

    apiKey: str = ""
    secretKey: str = ""

    status_code: int = None
    response: Union[str, dict] = None


class RestClient:

    def __init__(self, session: ClientSession = None):

        self.session = session

    async def init_session(self):
        if not self.session:
            self.session = ClientSession(trust_env=True)

    async def get_response(self, req: Request) -> Request:
        await self.init_session()
        if req.params:
            query: list = []
            for k, v in sorted(req.params.items()):
                query.append(k + "=" + str(v))
            query: str = '&'.join(query)
            path = req.host + req.api + "?" + query
            req.params = {}
        else:
            path = req.host + req.api
        log.info(f"request: {req}")
        try:
            cr: ClientResponse = await self.session.request(
                method=req.method,
                url=path,
                headers=req.headers,
                params=req.params,
                data=req.payload,
            )
            log.info(f"url: {cr.url}")
            req.status_code = cr.status
            req.response = await cr.text()
            # log.info(f"text, type: {type(req.response)} value: {req.response}")
            try:
                req.response = loads(req.response)
            except TypeError:
                pass
        except Exception as e:
            log.error(f"请求失败, url: {path}, err: {e}")
        log.info(f"status_code: {req.status_code}")
        log.info(f"path, {path}, response: {req.response}")
        return req

    async def get_response_single(
            self, method: str, host: str, api: str = "", params: dict = None, payload: dict = None, headers: dict = None
    ):
        ret = await self.get_response(req=Request(
            method=method, host=host, api=api, params=params, payload=payload, headers=headers
        ))
        return ret.status_code, ret.response


if __name__ == '__main__':
    pass

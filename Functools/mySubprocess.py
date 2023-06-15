# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/6/14 11:30

from asyncio import subprocess


async def MyAioSubprocess(cmd: str) -> str:
    p = await subprocess.create_subprocess_shell(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = await p.communicate()
    try:
        return out.decode().strip()
    except AttributeError:
        return ""


if __name__ == '__main__':
    import asyncio
    d = "ps -ef|grep p"
    r = asyncio.run(MyAioSubprocess(cmd=d))
    print(r)

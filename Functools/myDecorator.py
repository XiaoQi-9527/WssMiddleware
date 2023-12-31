# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2022/8/10 14:58

from loguru import logger as log


def ExDecorator(event="操作"):
    """异常装饰器"""
    def outer(func):
        def inner(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                # log.info(f"执行: {event}")
            except Exception as e:
                log.warning(f"{event} 异常, 原因: {e}")
                res = False
            return res
        return inner
    return outer


class PermDecorator:
    """权限装饰器"""

    def __init__(self, perm=False, on_finish=None):
        self.perm = perm
        self.on_finish = on_finish

    def __call__(self, func):
        def inner(*args, **kwargs):
            if self.perm:
                func(*args, **kwargs)
            else:
                self.on_finish(msg="没有权限")
        return inner


class InitDecorator:
    """格式化装饰器"""

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwarg):
        try:
            res = self.func(*args, **kwarg)
        except Exception as e:
            log.warning(f"异常, 原因: {e}")
            res = {}
        return res


if __name__ == '__main__':
    pass

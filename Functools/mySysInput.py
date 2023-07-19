# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/7/12 11:42

from typing import Optional, Any
import sys


def define(name: str, default: Optional[Any] = None, _type: Optional[type] = str):
    args = sys.argv[1:]
    try:
        ret = None
        for val in args:
            k, v = val.split("=")
            if k.replace("-", "") == name:
                ret = v
                break
        return _type(ret) if ret else default
    except Exception as e:
        print(e)
    finally:
        del args


if __name__ == "__main__":
    host = define(name="host", _type=str)
    print(host, type(host))
    prot = define(name="port", default=7891, _type=int)
    print(prot, type(prot))

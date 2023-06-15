# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/3/22 21:20

from dataclasses import dataclass


@dataclass
class FreeDataclass:

    def to_dict(self) -> dict:
        return self.__dict__


@dataclass(frozen=True)
class FrozenDataclass:

    def to_dict(self) -> dict:
        return self.__dict__


if __name__ == '__main__':
    pass

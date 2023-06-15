# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2022/8/23 14:33

from typing import Union

import pytz
import datetime


class MyDatetime:
    @staticmethod
    def dt2str(dt: datetime.datetime) -> str:
        """
        :param dt:  <class 'datetime.datetime'>
        :return: 2022-02-22 22:22:22
        """
        return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def dt2ts(dt: datetime.datetime, thousand: bool = True) -> int:
        """
        :param dt: <class 'datetime.datetime'>
        :param thousand: 是否需要转毫秒
        :return: 秒: 1645539742 | 毫秒: 1645539742000
        """
        if thousand:
            return int(dt.timestamp() * 1000)
        else:
            return int(dt.timestamp())

    @staticmethod
    def now() -> datetime.datetime:
        """
        :return: <class 'datetime.datetime'>
        """
        return datetime.datetime.now()

    @staticmethod
    def yesterday() -> datetime.datetime:
        """
        :return: <class 'datetime.datetime'>
        """
        return datetime.datetime.now() - datetime.timedelta(days=1)

    @staticmethod
    def now2str() -> str:
        """
        :return: 2022-02-22 22:22:22
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def utcnow2str() -> str:
        """
        :return: 2022-02-22T22:22:22
        """
        return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def utc2dt(dt: str) -> datetime.datetime:
        """
        :param dt: 2022-02-22T22:22:22.722
        :return: <class 'datetime.datetime'>
        """
        return datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f")

    @staticmethod
    def timestamp() -> float:
        """
        :return: 秒: 1645539742.000000
        """
        return datetime.datetime.now().timestamp()

    @staticmethod
    def ts2str(ts: Union[str, Union[float, int]], thousand: bool = True, chz: bool = False) -> str:
        """
        :param ts: 秒: 1645539742.000000 | 毫秒: 1645539742000.000
        :param thousand: 是否需要转毫秒
        :param chz:
        :return: 2022-02-22 22:22:22
        """
        ts = float(ts) / 1000 if thousand else float(ts)
        dt = datetime.datetime.fromtimestamp(ts)
        if chz:
            dt += datetime.timedelta(hours=8)
        return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def ts2dt(ts: Union[str, Union[float, int]], thousand: bool = True) -> datetime.datetime:
        """
        :param ts: 秒: 1645539742.000000 | 毫秒: 1645539742000.000
        :param thousand: 是否需要转毫秒
        :return: <class 'datetime.datetime'>
        """
        ts = float(ts) / 1000 if thousand else float(ts)
        return datetime.datetime.fromtimestamp(ts)

    @staticmethod
    def str2ts(dt: str, thousand: bool = True) -> int:
        """
        :param dt: 2022-02-22 22:22:22
        :param thousand: 是否需要转毫秒
        :return: 秒: 1645539742 | 毫秒: 1645539742000
        """
        if thousand:
            return int(datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
        else:
            return int(datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timestamp())

    @staticmethod
    def str2dt(dt: str) -> datetime.datetime:
        """
        :param dt: 2022-02-22 22:22:22
        :return: <class 'datetime.datetime'>
        """
        return datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def utc2bj(dt: datetime.datetime) -> datetime.datetime:
        return dt.astimezone(pytz.timezone('Asia/Shanghai'))

    @staticmethod
    def add8hr() -> datetime.datetime:
        return datetime.datetime.now() + datetime.timedelta(hours=8)


if __name__ == '__main__':
    pass

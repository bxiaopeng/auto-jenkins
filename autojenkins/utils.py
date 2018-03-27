# -*- coding:utf-8 -*-

"""
<Description> (utils.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Created by bixiaofan <wirelessqa@163.com> on 2018/3/27 at 下午8:27
"""
import arrow


def humanize(_time: str) -> str:
    """
    把时间转换成更人性化的时间
    :param  str _time: 可以是「时间戳」或「其他格式的时间」
    :return: str 更人性化的时间

    :usage:

    humanize(2017-11-26T11:06:22.636038+08:00) >> 3小时前
    humanize(1522153448) >> 几秒前
    """
    try:
        return arrow.get(_time).to('local').humanize(locale="zh")
    except Exception:
        return _time


def second2hms(seconds, delimiter: str = ':'):
    """
    秒数转换成 时:分:秒
    :param seconds:  秒数
    :param delimiter: 分隔符
    :return:时:分:秒

    usage:
    second2hms(137) ==》0:02:17
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    hms = "%02d:%02d:%02d" % (h, m, s)

    if delimiter != ":":
        hms = hms.replace(":", delimiter)

    return hms


def ms2hms(ms: int, delimiter: str = ':'):
    """
    毫秒数转换成 时:分:秒
    :param seconds:  秒数
    :param delimiter: 分隔符
    :return:时:分:秒

    :usage:
    ms2hms(137) ==》0:02:17
    """

    return second2hms(ms / 1000, delimiter)
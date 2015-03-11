#! /usr/bin/env python
# coding:utf-8

from mod import Mod
from datetime import datetime
import re
from collections import defaultdict
import numpy


class ModBurimiti(Mod):
    def __init__(
        self,
        logger=None,
    ):
        Mod.__init__(self, logger)

        self.basetime = datetime.now()
        self.time_flag = True

        self.burimiti_regex = re.compile(r"ﾌﾞﾘ|ﾘｭﾘｭ|ﾌﾞﾂ|ﾁﾁ|ﾐﾘ|([ｂｕｔｉｍｒ]){4,}")

        self.last_update = datetime.now()
        self.log = defaultdict(list)

    def is_fire(self, message, master) -> bool:
        now = datetime.now()
        if (now - self.last_update).days >= 1:
            self.log = defaultdict(list)
        self.last_update = now

        flag = True if self.burimiti_regex.search(message["text"]) and \
            message["user"]["screen_name"] != master["screen_name"] and\
            "retweeted_status" not in message \
            else False

        if flag:
            self.log[message["user"]["screen_name"]].append(datetime.now())

        return flag

    def reses(self, message, master):
        screen_name = message["user"]["screen_name"]
        name = message["user"]["name"]
        log = self.log[screen_name]
        count = len(log)

        profile = {
            "screen_name": screen_name,
            "name": name,
            "count": count,
        }

        if count % 10 == 0 and count >= 1:
            ret_lst = [
                "{name}の本日{count}回目のﾌﾞﾁﾐﾘを観測っ",
                "{name}がｵﾝﾗｲﾝでﾌﾞﾘﾐﾁ中っ本日{count}回目っ",
            ]
            if len(log) >= 2:
                ret_lst.append(
                    "{name}の本日{count}回目" +
                    str((log[-1] - log[-2]).seconds) +
                    "秒ぶりのﾌﾞﾁﾐﾘを観測っ"
                )

        return [
            (numpy.random.dirichlet((9, 1), 1).max(),
             fmt.format(**profile),
             "burimiti",
             {})
            for fmt in ret_lst
        ]

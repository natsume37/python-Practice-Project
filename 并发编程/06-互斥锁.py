# -*- coding: utf-8 -*-
"""
@File    : 06-互斥锁.py
@Author  : Martin
@Time    : 2025/9/29 9:27
@Desc    : 互斥锁 ：并行变串行
"""
import json
import random
from multiprocessing import Process, Lock

import time


# 查询车票
def search_ticket(name):
    with open('data/tickets.json', 'r', encoding='utf-8') as f:
        dic = json.load(f)
        print(f"用户{name}查询余票{dic.get("tickets_num")}")


# 买票
def buy_ticket(name):
    # 查询车票
    with open('data/tickets.json', 'r', encoding='utf-8') as f:
        dic = json.load(f)
    # 模拟网络延时
    time.sleep(random.randint(1, 5))
    if dic.get("tickets_num") > 0:
        dic["tickets_num"] -= 1
        with open('data/tickets.json', 'w', encoding='utf-8') as f:
            json.dump(dic, f)
        print(f"用户{name}买票成功")
    else:
        print(f"余票不足、用户{name}买票失败")


def task(name, mutex):
    search_ticket(name)
    # 抢锁  获得
    mutex.acquire()
    buy_ticket(name)
    # 释放锁  释放
    mutex.release()


if __name__ == '__main__':
    mutex = Lock()
    for i in range(1, 8):
        p = Process(target=task, args=(i, mutex))
        p.start()

    """
    用户2查询余票2
用户1查询余票2
用户3查询余票2
用户4查询余票2
用户5查询余票2
用户6查询余票2
用户7查询余票2
用户2买票成功
用户1买票成功
余票不足、用户3买票失败
余票不足、用户4买票失败
余票不足、用户5买票失败
余票不足、用户6买票失败
余票不足、用户7买票失败
    """

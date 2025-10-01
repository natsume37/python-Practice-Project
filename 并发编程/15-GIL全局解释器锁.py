# -*- coding: utf-8 -*-
"""
@File    : 15-GIL全局解释器锁.py
@Author  : Martin
@Time    : 2025/10/1 16:11
@Desc    : 
"""
from threading import Thread, Lock
import time

num = 180
mutex = Lock()


def task():
    global num
    mutex.acquire()
    temp = num
    # 通过注释掉模拟延迟，来验证GIL
    # time.sleep(0.5)
    num = temp - 1
    mutex.release()


if __name__ == '__main__':
    l = []
    for i in range(180):
        t = Thread(target=task)
        t.start()
        l.append(t)

    for t in l:
        t.join()
    print(num)
# 结果：0
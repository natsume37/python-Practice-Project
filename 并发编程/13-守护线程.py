# -*- coding: utf-8 -*-
"""
@File    : 13-守护线程.py
@Author  : Martin
@Time    : 2025/9/30 23:01
@Desc    : 主线程死了、守护线程也要死
t.daemon = True

主线程运行完毕后不会立即结束、而是等待所有子线程都结束后才结束
主线程结束意味着主线程所在的主进程结束了
"""

from threading import Thread
import time


def task(name):
    print(f"{name} 还活着")
    time.sleep(3)
    print(f"{name} 正常死亡")


if __name__ == '__main__':
    t = Thread(target=task, args=("妲己",))
    t.daemon = True
    t.start()
    print("纣王驾崩了")

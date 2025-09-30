# -*- coding: utf-8 -*-
"""
@File    : 02-join方法.py
@Author  : Martin
@Time    : 2025/9/29 8:35
@Desc    : join方法、让主进程等待子进程运行结束再继续执行
"""

from multiprocessing import Process
import time


def func(name, n):
    print(f"{name}开始执行")
    time.sleep(n)
    print(f"{name}开始执行")


if __name__ == '__main__':
    start = time.time()
    # p1 = Process(target=func, args=("1写论文", 1))
    # p2 = Process(target=func, args=("2写论文", 2))
    # p3 = Process(target=func, args=("3写论文", 3))
    # p1.start()
    # p2.start()
    # p3.start()
    l = []
    for i in range(1,4):
        p = Process(target=func, args=(f"写论文{i}", i))
        p.start()
        l.append(p)
    for p in l:
        p.join()
    print("主进程开始执行")
    end = time.time()
    print(end - start)
"""
代码无法直接创建进程、都是通知操作系统完成、所以顺序随机。
"""

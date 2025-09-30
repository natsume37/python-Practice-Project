# -*- coding: utf-8 -*-
"""
@File    : 08-IPC机制.py
@Author  : Martin
@Time    : 2025/9/30 21:11
@Desc    : 进程之间通讯
"""
from multiprocessing import Queue, Process


def task1(q):
    q.put("宫保鸡丁")


def task2(q):
    print(q.get())


if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=task1, args=(q,))
    p2 = Process(target=task2, args=(q,))
    p1.start()
    p2.start()
    # p.join()  # 不需要 拿不到数据会阻塞

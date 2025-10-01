# -*- coding: utf-8 -*-
"""
@File    : 16-多线程vs多进程.py
@Author  : Martin
@Time    : 2025/10/1 16:35
@Desc    : 
"""
# 计算密集型
from multiprocessing import Process
from threading import Thread
import time


def task():
    res = 0
    for i in range(10000000):
        res += i


if __name__ == '__main__':
    # os.cpu_count()  查看电脑是多少核
    l = []
    s = time.time()
    for i in range(8):
        p = Process(target=task)  # 1.623516321182251
        # p = Thread(target=task) # 4.271202802658081
        p.start()
        l.append(p)
    for p in l:
        p.join()
    e = time.time()
    print(e - s)

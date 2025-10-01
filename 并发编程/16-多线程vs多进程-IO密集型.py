# -*- coding: utf-8 -*-
"""
@File    : 16-多线程vs多进程-IO密集型.py
@Author  : Martin
@Time    : 2025/10/1 16:44
@Desc    : 
"""
# IO密集型
from multiprocessing import Process
from threading import Thread
import time


def task():
    time.sleep(1)


if __name__ == '__main__':
    # os.cpu_count()  查看电脑是多少核
    l = []
    s = time.time()
    for i in range(500):
        # p = Process(target=task)  # 31.658602952957153
        p = Thread(target=task) # 1.0385398864746094
        p.start()
        l.append(p)
    for p in l:
        p.join()
    e = time.time()
    print(e - s)

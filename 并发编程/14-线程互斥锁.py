# -*- coding: utf-8 -*-
"""
@File    : 14-线程互斥锁.py
@Author  : Martin
@Time    : 2025/10/1 14:33
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
    time.sleep(0.5)
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

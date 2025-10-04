# -*- coding: utf-8 -*-
"""
@File    : 18-递归锁.py
@Author  : Martin
@Time    : 2025/10/4 9:57
@Desc    : RLock
"""
from threading import Thread, RLock, current_thread
import time

# mutex1 等于 mutex2
mutex1 = mutex2 = RLock()


def task():
    mutex1.acquire()
    print(current_thread().name, "抢到锁1")
    mutex2.acquire()
    print("抢到锁2")
    mutex2.release()
    mutex1.release()
    task2()


def task2():
    mutex2.acquire()
    print(current_thread().name, "抢到锁2")
    time.sleep(1)
    mutex1.acquire()
    print("抢到锁1")
    mutex1.release()
    mutex2.release()


if __name__ == '__main__':
    for i in range(8):
        t = Thread(target=task)
        t.start()
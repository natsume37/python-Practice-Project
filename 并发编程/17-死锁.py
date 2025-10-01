# -*- coding: utf-8 -*-
"""
@File    : 17-死锁.py
@Author  : Martin
@Time    : 2025/10/1 16:53
@Desc    : 
"""
# 死锁
from threading import Thread, Lock, current_thread
import time

mutex1 = Lock()
mutex2 = Lock()


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
"""
Thread-1 (task) 抢到锁1
抢到锁2
Thread-1 (task) 抢到锁2
Thread-2 (task) 抢到锁1

阻塞了
"""

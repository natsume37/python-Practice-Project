# -*- coding: utf-8 -*-
"""
@File    : 19-信号量.py
@Author  : Martin
@Time    : 2025/10/4 10:13
@Desc    : Semaphore
用于限制进程的数量
"""
import random
from threading import Thread, Semaphore
import time

sp = Semaphore(5)

def task(name):
    sp.acquire()
    print(name,"抢到锁")
    time.sleep(random.randint(2,5))
    sp.release()

if __name__ == '__main__':
    for i in range(25):
        t = Thread(target=task, args=(f'宝马{i+1}',))
        t.start()
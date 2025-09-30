# -*- coding: utf-8 -*-
"""
@File    : 12-进程内数据共享.py
@Author  : Martin
@Time    : 2025/9/30 22:53
@Desc    : 
"""
from threading import Thread, current_thread, active_count
import os
"""
current_thread().name # 打印当前线程的名字（随机名）
active_count()： 活跃的线程数量（注意执行速度）
"""
age = 18


def task():
    print("子线程", os.getpid())
    global age
    age = 16


if __name__ == '__main__':
    t = Thread(target=task)
    t.start()
    # print("主线程", os.getpid())
    t.join()  # 保证子线程先执行
    print(age)

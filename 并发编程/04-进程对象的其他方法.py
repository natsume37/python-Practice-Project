# -*- coding: utf-8 -*-
"""
@File    : 04-进程对象的其他方法.py
@Author  : Martin
@Time    : 2025/9/29 8:53
@Desc    : 
"""
# pid号（进程号）：同一计算机、独一无二
# windows 查询进程号、tasklist|findstr <进程号>
from multiprocessing import Process, current_process
import time
import os


def task(name):
    # print(f"{current_process().pid}任务打印中") # 获取当前进程号pid
    print(f"{name}的进程号{os.getpid()}")  # 获取当前进程的pid
    print(f"{name}的父进程号{os.getppid()}")  # 获取父进程的pid
    time.sleep(100)


if __name__ == '__main__':
    p = Process(target=task, args=("子进程",))
    p.start()
    p.terminate()  # 杀死进程  Windows：taskkill  <pid> ,mac\linux  kill -9 <pid>
    time.sleep(0.001)
    print(p.is_alive())  # 打印进程存活状态  代码速度太快、可能操作系统还没来得及杀死进程
    print(f"主进程：{current_process().pid}")
    task("主进程")

"""
主进程：13088
主进程的进程号13088
主进程的父进程号6072  # pycharm进程
子进程的进程号3872
子进程的父进程号13088
"""

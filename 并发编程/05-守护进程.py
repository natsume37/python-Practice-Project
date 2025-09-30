# -*- coding: utf-8 -*-
"""
@File    : 05-守护进程.py
@Author  : Martin
@Time    : 2025/9/29 9:15
@Desc    : 
"""
import time
# 守护进程 ：主进程活、子进程活、主进程死、守护进程也必须死

from multiprocessing import Process


def task(name):
    print(f"{name}还活着")
    time.sleep(3)
    print(name, "killed")


if __name__ == '__main__':
    p = Process(target=task, kwargs={'name': "妲己"})
    p.daemon = True  # 设置守护进程、必须在启动进程前设置！！！
    p.start()
    time.sleep(1)
    print("主进程死亡")

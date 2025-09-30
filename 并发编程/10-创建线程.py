# -*- coding: utf-8 -*-
"""
@File    : 10-创建线程.py
@Author  : Martin
@Time    : 2025/9/30 22:18
@Desc    :
进程：资源单位
线程：执行单位

一个进程自带一个线程、同一进程下线程的数据资源是共享的

- 线程消耗的资源更小
"""
from multiprocessing import Process
from threading import Thread
import time

# # 创建线程方法1
# def task(name):
#     print(f"{name} 任务开始")
#     time.sleep(3)
#     print(f"{name} 任务结束")
#
#
# if __name__ == '__main__':
#     t = Thread(target=task, args=("悟空",))
#     t.start()
#     print("主线程")
"""
线程不需要申请内存空间、不需要拷贝代码、资源消耗比创建进程少很多、可以不用写在__main__下
"""


class MyThread(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print(f"{self.name} 任务开始")
        time.sleep(3)
        print(f"{self.name} 任务结束")


if __name__ == '__main__':
    t = MyThread("悟空")
    t.start()
    print("主线程")

"""
t.join()
"""
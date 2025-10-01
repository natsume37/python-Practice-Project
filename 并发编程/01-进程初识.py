# -*- coding: utf-8 -*-
"""
@File    : 01-进程初识.py
@Author  : Martin
@Time    : 2025/9/28 22:12
@Desc    : 
"""

"""
创建进程的方法
os.fork()  :调用底层的fork()方法、但是Windows不支持
multiprocessing :主要用
subprocess：功能少点、运维用的多
"""
# 方法一
from multiprocessing import Process
import time


def func(name):
    print(f"{name}任务开始")
    time.sleep(5)
    print(f"{name}任务结束")

# windows必须加这个、要不然报错
if __name__ == '__main__':
    """
    windows创建子进程的方式是导入模块的模式、所以牵扯循环导入的问题。
    """
    # 1、进程操作对象
    p = Process(target=func, args=("子线程",))
    # 2、创建进程
    p.start()
    print("主进程")

# 方式二 类方式
from multiprocessing import Process
import time


class MyProcess(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print(f"{self.name}开始")
        time.sleep(5)
        print(f"{self.name}结束")


if __name__ == '__main__':
    p = MyProcess("子进程")
    p.start()
    print("主进程开始")

"""
开辟子进程相当于再内存里申请一块内存空间、然后将代码放在里面执行、进程之间的数据没法直接互通、需要借助第三方工具。
"""

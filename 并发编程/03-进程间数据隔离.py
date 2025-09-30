# -*- coding: utf-8 -*-
"""
@File    : 03-进程间数据隔离.py
@Author  : Martin
@Time    : 2025/9/29 8:49
@Desc    : 
"""
from multiprocessing import Process

age = 18

def func():
    global age
    age = 16

if __name__ == '__main__':
    p = Process(target=func)
    p.start()
    p.join()
    print(age)
    # 18 :主进程并没有被修改
# -*- coding: utf-8 -*-
"""
@File    : 05-yield简介.py
@Author  : Martin
@Time    : 2025/10/13 18:15
@Desc    : 
"""


def f1():
    yield 1
    yield 2


g = f1()
print(next(g))  # 1
print(next(g))  # 2
# print(next(g))  # StopIteration异常
g = f1()
for i in g:
    print(i)


def f4():
    res = yield "右边的值"
    yield res



g4 = f4()  # 生成器对象
print(next(g4))
print(g4.send("左边res的值"))
"""
右边的值
左边res的值
"""


# -*- coding: utf-8 -*-
"""
@File    : 06-yeild-form.py
@Author  : Martin
@Time    : 2025/10/13 18:30
@Desc    : 
"""


# yield form
def f5():
    for i in "abc":
        yield i
    for j in range(3):
        yield j

    # 等价于
    yield from "abc"
    yield from range(3)


for i in f5():
    print(i)


# 第二个作用
def sub():
    yield 1
    yield 2
    yield 3


def link():
    res = yield from sub()
    print('结果', res)

g = link()
print(next(g))
print(next(g))
print(next(g))
print(next(g))

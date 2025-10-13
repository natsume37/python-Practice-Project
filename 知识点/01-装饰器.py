# -*- coding: utf-8 -*-
"""
@File    : 01-装饰器.py
@Author  : Martin
@Time    : 2025/10/13 12:54
@Desc    : 装饰器在不修改原函数的情况下给函数添加特定功能

无参装饰器模板
def outer(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return res
    return wrapper
# 本质是替换（把原来的变量地址的内容替换成我们修改后的代码
@outer --->  func = outer(func)
"""
import time

def runtime(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return res
    return wrapper

# 无参装饰器  （语法糖只能传一个参数）
# @runtime  # hello = runtime(hello)
# def hello():
#     print('hello')
#
# hello()

# 有参装饰器
def sleep_time(t):
    def outer(func):
        def wrapper(*args, **kwargs):
            # 延时指定时间
            time.sleep(t)
            res = func(*args, **kwargs)
            return res
        return wrapper
    return outer
@sleep_time(3)  # --> @outer  ->hello = outer(hello)
def hello():
    print('hello')
hello()
# -*-coding:utf-8 -*-

"""
# File:         02迭代器.py
# Time:         2025/8/6 16:53
# Author:       Martin
# Description:  
"""
# 迭代器
# 节省内存资源

# 可迭代对象：只要内置有__iter__()方法的对象都是可迭代对象。

# d = {'key1':'1','key2':'2'}
# 变为可迭代对象
# res = d.__iter__()
#
# print(res.__next__())
# print(res.__next__())
# print(res.__next__())

# 多调用了一次 会报错。

# 不通过for循环实现循环取值

# while True:
#     try:
#         print(res.__next__())
#     except StopIteration:
#         break

# 迭代器对象：内置有__next__()和__iter__()方法（文件对象）
# 迭代器调用__next__()方法，就会得到迭代器的下一个值
# 迭代器调用__iter__()方法、得到的是迭代器本身

# s = {1,2,3}
# res = s.__iter__()
# print(res.__iter__() is res)
# True
# 这种设计是兼容for循环的
# for i in 迭代器对象.__iter():
# for i in 迭代器对象.__iter():

# 生成器
# 自定义迭代器

# def func():
#     print("第一次执行")
#     yield 1
#     print("第二次执行")
#     yield 2
#     print("第三次执行")
#     yield 3
#     print("第四次执行")
#     yield 4
#     print("第五次执行")
# res = func()
# res.__iter__()
# 两种写法都行
# res=res.__next__()
# res = next(res)
# print(res)
# 第一次执行
# 1

# yield表达式
def func(x):
    print(f"{x}开始执行")
    while True:
        y = yield None
        print('\n', x, y, '\n')

g = func(1)
# res = next(g)
# print(res)
# next(g)

g.send(None) # next(g)
# next(g)
g.send(10)

g.send(20)
# -*- coding: utf-8 -*-
"""
@File    : 12-反射机制.py
@Author  : Martin
@Time    : 2025/10/16 11:24
@Desc    : 反射机制：电脑如何知道这个对象有没有这个属性？----> 程序动态分析的能力

hasattr()
getattr()
setattr()
delattr()
"""


# def f1(obj):
#     obj.age
#
# f1(18) # AttributeError: 'int' object has no attribute 'age'
#

# def f1(obj):
#     if 'age' not in obj:
#         return
#     obj.age
#
# f1(18) # AttributeError: 'int' object has no attribute 'age'
#  并不是所有的对象都能调用 __dict__方法

class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show_info(self):
        print(self.name, self.age)


obj = Human('Martin', 18)
"""
...
过了很久、你忘了obj返回的是啥了
"""

# 不是所有的对象都可以访问__dict__ 但是有内置方法 dir() 当然一般不用（返回的字符串）
print(dir(obj))
"""
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__firstlineno__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__static_attributes__', '__str__', '__subclasshook__', '__weakref__', 'age', 'name', 'show_info']
"""
# hasattr()
# getattr()
# setattr()
# delattr()
# print(hasattr(obj, 'age'))  # True
# print(getattr(obj, 'name'))  # Martin
# setattr(obj, 'name', "李白")
# print(obj.name) # 李白
# print(delattr(obj, 'age'))
#
# print(getattr(18, 'age', None))
#


class Ftp:
    def put(self):
        print("正在上传数据")
    def get(self):
        print("正在下载数据")
    def interact(self):
        opt  = input(">>>")
        if hasattr(self, opt):
            getattr(self, opt)()
        else:
            print("功能不存在")
obj = Ftp()
obj.interact()
# -*- coding: utf-8 -*-
"""
@File    : 16-元类实现单例模式.py
@Author  : Martin
@Time    : 2025/10/16 22:57
@Desc    : 
"""


class SingletonMeta(type):
    _instance = {}  # 存放示例对象

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            instance = super().__call__(*args, **kwargs)
            cls._instance[cls] = instance
        return cls._instance[cls]


class Test(metaclass=SingletonMeta):
    def __init__(self,value):
        self.value = value


a = Test(1)
b = Test(2)
print(a is b)
print(a.value)
print(b.value)
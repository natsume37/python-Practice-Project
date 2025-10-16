# -*- coding: utf-8 -*-
"""
@File    : 07-MixIns机制-多继承.py
@Author  : Martin
@Time    : 2025/10/15 22:39
@Desc    :
MixIns：通过命名规范提高代码可读性、区分（更能类（单纯解决某些特定功能的类）、父类）
1.用来表达某一种功能、而不是事物！
2.功能单一（类似于插件）
"""


# MixIns机制
class Fowl:  # 家禽类
    pass


class SwimMixIn: # 用来表达某一种功能、而不是事物！
    def swimming(self):
        pass


class Chicken(Fowl):
    pass


class Duck(SwimMixIn, Fowl):
    pass


class Goose(SwimMixIn, Fowl):
    pass

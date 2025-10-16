# -*- coding: utf-8 -*-
"""
@File    : 10-抽象基类.py
@Author  : Martin
@Time    : 2025/10/16 11:04
@Desc    : 抽象基类
让父类成为一个规范标准

当然python推崇的还是鸭子类型：在代码层面规范开发者
"""

import abc


# 抽象基类
class car(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self):
        pass


"""
只要子类继承了父类、必须自己定义一个run方法、要不然直接报错！
且抽象基类不能直接实例化！
"""


class xiaomi(car):
    def run(self):
        pass
    # 正常运行


class lix(car):
    pass
    # 报错

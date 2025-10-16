# -*- coding: utf-8 -*-
"""
@File    : 09-鸭子类型.py
@Author  : Martin
@Time    : 2025/10/16 10:55
@Desc    : python多态的使用
主要还是通过代码规范来而不是强制限制、不用继承也能达到统一接口的目的、解耦合的效果
长的像就行
"""


class car:
    def run(self):
        print('run')


# 不继承父类、通过代码规范、达到统一接口的目的
class xiaomi:
    def run(self):
        print('充电')


class lix:
    def run(self):
        print('换电')


def driver_car(obj):
    obj.run()


# 鸭子类型
# linux：一切皆文件
"""
让它们长的像
"""


class Disk:
    def read(self):
        print('Disk read')

    def write(self):
        print('Disk write')


class Memory:
    def read(self):
        print('Memory read')

    def write(self):
        print('Memory write')


class Txt:
    def read(self):
        print('Txt read')

    def write(self):
        print('Txt write')


def openfile(obj):
    obj.read()
    obj.write()

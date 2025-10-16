# -*- coding: utf-8 -*-
"""
@File    : 08-super关键字.py
@Author  : Martin
@Time    : 2025/10/16 10:31
@Desc    : 
"""


class Human:
    star = 'earth'

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender


class Chinese(Human):
    # star = 'earth'
    nation = 'China'

    def __init__(self, name, age, gender, balance):
        # super 会参照当前类(obj)的MRO列表、找下一个类的init方法（自动传self)
        # Human.__init__(self, name, age, gender) # 方法一
        # super(Chinese, self).__init__(name, age, gender) # python2 必须这样写（兼容python2）
        super().__init__(name, age, gender)  # 方法二 python3写法
        self.balance = balance

    def speak_chinese(self):
        print(f'{self.name}在说普通话')


class American(Human):
    # star = 'earth'
    nation = 'American'

    # def __init__(self, name, age, gender):
    #     self.name = name
    #     self.age = age
    #     self.gender = gender

    def speak_english(self):
        print(f'{self.name}speak english')
